#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""This class is the underlaying class for all ODE models
   It has the minimum params, etc set and functions to solve and
   plot data
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
from scipy.optimize import fsolve
from itertools import product
from scipy.stats import qmc

class CoralODELab: # pylint: disable=invalid-name
    """This is a top-level class to use as an inherit class for all other models. We use it
    to solve ODE sets to describe the interactions of coral-algae on reefs. 

    :param model_name: Name given to this model
    :type name: string
    :param output: holder for the output of the solver
    :type output: list[float]
    :param times: number of years model is being run for
    :type times: list[float]
    :param start_conditions: inital population of z(0) (coral) and z(1) (algae) adding up to 1
    :type start_conditions: list[float]
    :param parameters: variable names and value
    :type parameters: dictionary[string:int]
    :param num_parameters: total number of parameters in model
    :type num_parameters: [int]
    :param citation: full citation of paper model was extracted from
    :type param: [string]
    :param parameter_names: definition of each parameter symbol
    :type parameter_names: dictionary[string:string]
    :param parameter_range: values each parameter can be observed at
    :type parameter_range: dict[string: range]
    
    """

    def __init__(self, model):
        """Constructor method
        """
        self.model_name = model
        self.output = []
        self.times = []
        self.start_conditions = []
        self.parameters = {}
        self.num_parameters = 0
        self.num_eq = 0
        self.citation = ""
        self.parameter_names = {}
        self.parameter_range = {}
        self.coral_cover = 0
        self.macroalgae_cover = 0
        self.turfalgae_cover = 0
        self.p = False

        # internal variables
        self._coral_colour  = "#F88379"
        self._malgae_colour = "#617D48"
        self._algae_colour  = "#617D48"
        self._talgae_colour = "#5FC87E"
        self._space_colour  = "#9aa69d"

    def _check_value(self,number):

        if isinstance(number,list):
            for l in number:
                if not isinstance(l, (float, int)):
                    raise TypeError("Value entered in list is not an integer or float")
                if l < 0:
                    raise ValueError("Value entered in list is negative, \
                                    please insert positive number")
        elif isinstance(number, (float, int)):
            if number < 0:
                raise ValueError("Value entered is negative, please insert positive number")
        else:
            raise TypeError("Value entered is not an integer or float")


    def _check_length(self, my_list, expected_length):

        if len(my_list) != expected_length:
            raise TypeError("Entered wrong number of parameters")


    # this forces you to create an ode function
    # in every class that inherits this one
    def ode(self, z, t): # ode gets changed to whatever model is being run
        """
        Solve the ODE equation set.

        Return array of the dX/dt value for each ODE. Used by scipy.odeint

        :param z: List of starting conditions. One per ODE
        :type z: list[float]
        :param t: list of years ODE is run for
        :type t: list[float]
        :raise: Exception if ODEs not implemented
        :return: delta values
        :rtype: list[float]
        
        """

        raise NotImplementedError

    def set_times(self,times):
        """
        Set how many years the model will run for, enter first and last year, 
        e.g (0,10) for 10 years
        
        :param times: number of years model is being run for
        :type times: list[float]
        
        """

        self._check_length(times,2)
        self._check_value(times)
        if not sorted(times) == times:
            raise ValueError("Times should be in ascending order")

        self.times = np.arange(times[0], times[1]+1, 1)


    def set_start_conditions(self, start_conditions):
        """
        Set the intial population cover of z(0) and z(1) (and z(2)). Values must add up to 1
        
        :param start_conditions: list of values for the start of the model. 1 per equation
        :type start_conditions: list[float]
        
        """

        self._check_length(start_conditions,self.num_eq)
        self._check_value(start_conditions)

        if sum(start_conditions) > 1:
            raise ValueError("Sum of starting conditions should be between 0 and 1")

        self.start_conditions = start_conditions
        self.coral_cover = start_conditions[0]
        self.macroalgae_cover = start_conditions[1]
        if self.num_eq == 3:
            self.turfalgae_cover = start_conditions[2]

    def solve_time(self, start=None):
        """
        Solves the ODE over the times specified by the user. Stores output in self.output

        :return: self.output
        
        """
        if start is None:
            start = self.start_conditions
        # run the scipy ode integrator
        self.output = odeint(self.ode, start, self.times)

        # set a limit of outputs to be between 0 and 1
        self.output = np.clip(self.output, 0, 1)

        self.coral_cover = self.output[-1][0]
        self.macroalgae_cover = self.output[-1][1]
        if self.num_eq == 3:
            self.turfalgae_cover = self.output[-1][2]

        return self.output


    def plot_through_time(self, filename=None):
        """
        Plotting graph for population change (y axis) and time (x axis)
         
        """

        if len(self.output) < 1:
            return

        # plot the results
        plt.plot(self.times, self.output[:,0], label="Coral", color=self._coral_colour)
        if self.num_eq == 2:
            plt.plot(self.times, self.output[:,1], label="Algae", color=self._malgae_colour)
        elif self.num_eq == 3:
            plt.plot(self.times, self.output[:,1], label="Turf algae", color=self._talgae_colour)
            plt.plot(self.times, self.output[:,2], label="Macroalgae", color=self._malgae_colour)

        plt.ylim(0,1)
        plt.xlim(-1)
        plt.legend()
        plt.title(self.model_name)
        plt.xlabel('Time (years)')
        plt.ylabel('% cover')
        if filename is None:
            plt.show()
        else:
            #save figure
            pass

    def plot_bifurcation(self, parameter, ax=None, legend_loc='best'):
        """
        Create a bifurcation plot, with % cover of all species on the y axis 
        and the parameter on the x axis. 
        """
        import matplotlib.pyplot as plt
        import matplotlib.lines as mlines
        import numpy as np

        # If no axis is provided, create a new figure
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 6))

        # get parameter range
        param_range = np.linspace(self.parameter_range[parameter][0],
                                  self.parameter_range[parameter][1], 151)

        all_roots = []
        types = []
        # loop through param range
        for p in param_range:
            self.set_parameters(**{parameter: p})
            roots, type_root = self.find_eq_points()
            all_roots.append(roots)
            types.append(type_root)

        # Plot the roots
        for rr, tr, p in zip(all_roots, types, param_range):
            for r, t in zip(rr, tr):
                if "Stable" in t:
                    m_style, alpha_val = 'o', 1.0
                else:
                    m_style, alpha_val = 'x', 0.3

                ax.plot(p, r[0], marker=m_style, color=self._coral_colour, 
                        markersize=3, alpha=alpha_val, linestyle='None')
                
                if self.num_eq == 2:
                    ax.plot(p, r[1], marker=m_style, color=self._malgae_colour, 
                            markersize=3, alpha=alpha_val, linestyle='None')
                elif self.num_eq == 3:
                    ax.plot(p, r[1], marker=m_style, color=self._talgae_colour, 
                            markersize=3, alpha=alpha_val, linestyle='None')
                    ax.plot(p, r[2], marker=m_style, color=self._malgae_colour, 
                            markersize=3, alpha=alpha_val, linestyle='None')

        ax.set_xlim(param_range[0], param_range[-1])
        ax.set_ylim(-0.05, 1.05)
        ax.set_xlabel(self.parameter_names.get(parameter, parameter).capitalize())
        ax.set_ylabel('% cover')

        # Custom Legend Handles
        handles = [mlines.Line2D([], [], color=self._coral_colour, marker='o', linestyle='None', label='Coral')]
        if self.num_eq == 2:
            handles.append(mlines.Line2D([], [], color=self._malgae_colour, marker='o', linestyle='None', label='Algae'))
        elif self.num_eq == 3:
            handles.append(mlines.Line2D([], [], color=self._talgae_colour, marker='o', linestyle='None', label='Turf algae'))
            handles.append(mlines.Line2D([], [], color=self._malgae_colour, marker='o', linestyle='None', label='Macroalgae'))
        
        handles.append(mlines.Line2D([], [], color='black', marker='o', linestyle='None', label='Stable (Node)'))
        handles.append(mlines.Line2D([], [], color='black', marker='x', alpha=0.5, linestyle='None', label='Unstable'))

        ax.legend(handles=handles, loc=legend_loc)
        return ax

    def classify_stability(self,eigenvalues):
        """
        Classifies the stability of a root based on its eigenvalues.
        """
        real_parts = np.real(eigenvalues)
        imag_parts = np.imag(eigenvalues)
        
        n = len(real_parts)
        pos = np.sum(real_parts > 1e-6)
        neg = np.sum(real_parts < -1e-6)
        has_spirals = np.any(np.abs(imag_parts) > 1e-6)

        # 1. Stable Sink
        if neg == n:
            return "Stable Focus" if has_spirals else "Stable Node"
        
        # 2. Unstable Source
        if pos == n:
            return "Unstable Focus" if has_spirals else "Unstable Source"
        
        # 3. Saddle Points
        if pos > 0 and neg > 0:
            return f"Saddle ({pos} out, {neg} in)"
        
        # 4. Neutral / Center
        return "Neutral/Center"

    def generate_simplex_lhs(self, dim, n_samples):
        """
        Generates n_samples in `dim` dimensions such that:
        x_i >= 0  AND  sum(x_i) <= 1
        without discarding any invalid samples.
        """
        # 1. Sample in (dim + 1) dimensions to account for the slack variable
        sampler = qmc.LatinHypercube(d=dim + 1)
        u = sampler.random(n=n_samples)
        
        # 2. Avoid numerical issues with log(0)
        u = np.clip(u, 1e-12, 1.0 - 1e-12)
        
        # 3. Transform uniform samples into exponential variables
        e = -np.log(u)
        
        # 4. Normalize across the rows so each row sums to 1.0
        y = e / np.sum(e, axis=1, keepdims=True)
        
        # 5. Drop the last (slack) column. 
        # The remaining `dim` columns naturally sum to <= 1.0.
        return y[:, :dim]

    def find_eq_points(self, num_samples=1000):
        all_roots = []
        stability = []
        
        # 1. Generate guaranteed valid guesses inside the simplex
        initial_guesses = self.generate_simplex_lhs(self.num_eq, num_samples)
        
        # 2. Loop directly over valid guesses (100% acceptance rate)
        for start_init in initial_guesses:
            roots, infodict, ier, mesg = fsolve(
                self.ode, 
                start_init, 
                args=(0),
                fprime=self.analytical_jacobian,
                full_output=True
            )
            
            if ier in [1, 2, 3, 4]:
                Jacobian = self.analytical_jacobian(roots)
                if not np.isnan(Jacobian).any():
                    eigenvalues = np.linalg.eigvals(Jacobian)
                    label = self.classify_stability(eigenvalues)
                    all_roots.append(roots)
                    stability.append(label)   
            
        if not all_roots:
            return np.array([]), []

        # 5. Clean and find unique roots
        all_roots = np.array(all_roots).round(decimals=6)
        # Filter: must be positive and sum <= 1
        mask = np.all(all_roots >= 0, axis=1) & (np.sum(all_roots, axis=1) <= 1.001)
        all_roots = all_roots[mask]
        stability = np.array(stability)[mask]
        
        unique_roots, indices = np.unique(all_roots, axis=0, return_index=True)
        unique_stability = stability[indices]

        return unique_roots, unique_stability


    def plot_phase_space(self, grid_density=6, t_end=100):
        """
        Plots trajectories from various starting points and overlays equilibrium points.
        Works for 2D or 3D (as a 2D projection or 3D plot).
        """
        import matplotlib.pyplot as plt
        from itertools import product

        # 1. Setup Plot (2D vs 3D)
        fig = plt.figure(figsize=(10, 8))
        is_3d = self.num_eq == 3
        ax = fig.add_subplot(111, projection='3d' if is_3d else None)

        # 2. Generate Starting Conditions (Simplex-aware)
        axis = np.linspace(0.1, 0.9, grid_density)
        start_conditions = [p for p in product(axis, repeat=self.num_eq) if sum(p) <= 1.0]

        # 3. Solve and Plot Trajectories
        t_span = np.linspace(0, t_end, 500)
        for init in start_conditions:
            sol = odeint(self.ode, init, t_span)
            
            if is_3d:
                ax.plot(sol[:, 0], sol[:, 1], sol[:, 2], "k", alpha=0.3, lw=0.5)
                # Add a small arrow/marker at the start to show direction
                ax.scatter(sol[0,0], sol[0,1], sol[0,2], color='k', s=2, alpha=0.3)
            else:
                ax.plot(sol[:, 0], sol[:, 1], "k", alpha=0.4, lw=0.6)
                # Directional arrow at the start
                dx, dy = sol[5, 0] - sol[0, 0], sol[5, 1] - sol[0, 1]
                ax.arrow(sol[0, 0], sol[0, 1], dx, dy, shape='full', lw=0, 
                         length_includes_head=True, head_width=.015, color='k', alpha=0.4)

        # 4. Use your new find_eq_points()
        roots, stability_types = self.find_eq_points()

        # Map the new string labels to colors
        color_map = {
            "Stable Node": "green",
            "Stable Focus": "darkgreen",
            "Unstable Source": "red",
            "Unstable Focus": "darkred",
            "Neutral/Center": "gray"
        }

        for root, label in zip(roots, stability_types):
            # Determine color: blue for any kind of saddle, otherwise use map
            color = "blue" if "Saddle" in label else color_map.get(label, "black")
            
            if is_3d:
                ax.scatter(root[0], root[1], root[2], color=color, s=80, edgecolors='w', zorder=5)
            else:
                ax.plot(root[0], root[1], 'o', color=color, markersize=8, markeredgecolor='w', zorder=5)

        # 5. Final Formatting
        if is_3d:
            # Draw the C + T + M = 1 plane boundary
            ax.plot([1, 0, 0, 1], [0, 1, 0, 0], [0, 0, 1, 0], 'r--', alpha=0.2)
        ax.set_xlabel('Coral (C)')
        ax.set_ylabel('Turf (T)' if not is_3d else 'Turf (T)')
        if is_3d: ax.set_zlabel('Macroalgae (M)')
        
        plt.title(f"Phase Space Analysis ({self.num_eq}D)")
        ax.legend(loc="best")
        plt.tight_layout()
        plt.show()

    def plot_roots_3d(self, unique_roots, stability_types):
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # 1. Define Color Map for Stability
        color_map = {
            "Stable Node": "green",
            "Stable Focus": "darkgreen",
            "Unstable Source": "red",
            "Unstable Focus": "darkred",
            "Neutral/Center": "gray"
        }
        
        # 2. Plot the Boundary Simplex (C + T + M = 1)
        # This helps visualize the "ceiling" of the ecological space
        verts = [
            [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 0, 0]
        ]
        x, y, z = zip(*verts)
        ax.plot(x, y, z, color='black', alpha=0.3, linestyle='--', label="Simplex Boundary")

        # 3. Plot each root
        for root, stab in zip(unique_roots, stability_types):
            # Determine color based on stability label
            # (Handles "Saddle (x out, y in)" by checking if 'Saddle' is in the string)
            color = "blue" if "Saddle" in stab else color_map.get(stab, "black")
            
            ax.scatter(root[0], root[1], root[2], 
                       color=color, s=100, edgecolors='white', label=stab)

        # 4. Formatting
        ax.set_xlabel('Coral (C)')
        ax.set_ylabel('Turf (T)')
        ax.set_zlabel('Macroalgae (M)')
        ax.set_title('Equilibrium Points in C-T-M Space')
        
        # Remove duplicate labels in legend
        handles, labels = ax.get_legend_handles_labels()
        unique_labels = dict(zip(labels, handles))
        ax.legend(unique_labels.values(), unique_labels.keys(), loc='upper left')

        plt.show()

    def plot_cross_section(self, fixed_var='T', fixed_val=0.4, grid_density=10, t_end=100):
        """
        Plots a 2D slice of the 3D phase space and overlays projected equilibrium points.
        """
        import matplotlib.pyplot as plt
        from scipy.integrate import odeint

        # 1. Coordinate Mapping
        mapping = {'C': 0, 'T': 1, 'M': 2}
        fixed_idx = mapping[fixed_var]
        other_indices = [i for i in range(3) if i != fixed_idx]
        labels = list(mapping.keys())
        
        fig, ax = plt.subplots(figsize=(9, 7))

        # 2. Plot Trajectories on the Slice
        axis = np.linspace(0.02, 1.0 - fixed_val - 0.02, grid_density)
        t_span = np.linspace(0, t_end, 400)

        for val1 in axis:
            for val2 in axis:
                if val1 + val2 + fixed_val <= 1.0:
                    init = [0, 0, 0]
                    init[fixed_idx] = fixed_val
                    init[other_indices[0]] = val1
                    init[other_indices[1]] = val2
                    
                    sol = odeint(self.ode, init, t_span)
                    ax.plot(sol[:, other_indices[0]], sol[:, other_indices[1]], 
                            "k", alpha=0.2, lw=0.5)

        # 3. Get and Project Equilibrium Points
        roots, stability_types = self.find_eq_points()
        
        for root, label in zip(roots, stability_types):
            # Determine color based on stability string
            if "Stable" in label:
                color = "#2ecc71" # Green
                marker = '*'
            elif "Unstable" in label:
                color = "#e74c3c" # Red
                marker = 'o'
            else: # Saddles
                color = "#3498db" # Blue
                marker = 'D'
                
            # Calculate distance from the slice to set transparency
            dist_from_slice = abs(root[fixed_idx] - fixed_val)
            # Only show roots within a reasonable 'viewing distance'
            if dist_from_slice < 0.2:
                alpha = max(0.2, 1.0 - (dist_from_slice * 4)) # Closer = more solid
                
                ax.scatter(root[other_indices[0]], root[other_indices[1]], 
                           color=color, s=150, edgecolors='black', 
                           marker=marker, alpha=alpha, zorder=5, label=label)
                
                # Label the root if it's very close to the slice
                if dist_from_slice < 0.05:
                    ax.text(root[other_indices[0]]+0.02, root[other_indices[1]]+0.02, 
                            label, fontsize=8, fontweight='bold', alpha=alpha)

        # 4. Simplex Constraint Line (The 'Wall' where C + T + M = 1)
        # On our slice, the limit is: Var1 + Var2 = 1 - fixed_val
        limit = 1.0 - fixed_val
        ax.plot([0, limit], [limit, 0], 'r--', lw=1.5, label="Physical Limit")

        # Formatting
        ax.set_xlabel(f"Projected {labels[other_indices[0]]}")
        ax.set_ylabel(f"Projected {labels[other_indices[1]]}")
        ax.set_title(f"2D Phase Slice (Fixed {fixed_var} = {fixed_val})")
        ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        
        # Clean up legend (remove duplicates)
        handles, plot_labels = ax.get_legend_handles_labels()
        by_label = dict(zip(plot_labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc='upper right', fontsize='small')

        plt.tight_layout()
        plt.show()        

    def calculate_basins(self, grid_density=20, t_end=500):
        """
        Determines which stable equilibrium each point in the simplex evolves toward.
        """
        # 1. Get only the stable roots (the 'attractors')
        roots, stability = self.find_eq_points()
        stable_roots = roots[np.array([s == "Stable Node" or s == "Stable Focus" for s in stability])]
        
        if len(stable_roots) == 0:
            return "No stable attractors found."

        # 2. Create the grid
        axis = np.linspace(0.02, 0.98, grid_density)
        points = []
        labels = []
        
        t_span = np.linspace(0, t_end, 2) # We only care about the final state

        for combination in product(axis, repeat=self.num_eq):
            if sum(combination) <= 1.0:
                # 3. Integrate from this point
                # We use a long t_end to ensure it reaches equilibrium
                sol = odeint(self.ode, combination, t_span)
                final_state = sol[-1]
                
                # 4. Find the closest stable root (Euclidean distance)
                distances = [np.linalg.norm(final_state - root) for root in stable_roots]
                closest_root_index = np.argmin(distances)
                
                # Only count it if it actually reached the root (within tolerance)
                if distances[closest_root_index] < 1e-2:
                    points.append(combination)
                    labels.append(closest_root_index)

        return np.array(points), np.array(labels), stable_roots

    def calculate_basin_volumes(self, points, labels, stable_roots):
        """
        Calculates the percentage of the 3D simplex volume occupied by each attractor.
        """
        total_points = len(labels)
        volumes = {}
        
        # Identify which stable root is the 'Coral' one
        # (Assuming the root with the highest Coral value is index 0 or similar)
        for i, root in enumerate(stable_roots):
            count = np.sum(labels == i)
            percentage = (count / total_points) * 100
            
            # Create a descriptive key based on the root coordinates
            # e.g., "Attractor at C=0.8, T=0.1, M=0.1"
            key = f"Root {i} (C:{root[0]:.2f}, T:{root[1]:.2f}, M:{root[2]:.2f})"
            volumes[key] = percentage

        return volumes
    
    def plot_basins_3d(self):
        points, labels, stable_roots = self.calculate_basins()
        volumes = self.calculate_basin_volumes(points, labels, stable_roots)

        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')
        
        # 1. Colors and labels
        basin_colors = ['#2ecc71', '#e74c3c', '#3498db', '#f1c40f'] # Green, Red, Blue, Yellow
        
        # 2. Plot the Simplex Boundary
        boundary = np.array([[1,0,0], [0,1,0], [0,0,1], [1,0,0]])
        ax.plot(boundary[:,0], boundary[:,1], boundary[:,2], 'k-', alpha=0.4, lw=1.5)

        # 3. Plot Basin Clouds (The territories)
        for i, root in enumerate(stable_roots):
            mask = (labels == i)
            if np.any(mask):
                ax.scatter(points[mask, 0], points[mask, 1], points[mask, 2], 
                           color=basin_colors[i % len(basin_colors)], 
                           alpha=0.2, s=5)
            
            # 4. Plot Stable Attractors (The Stars)
            ax.scatter(root[0], root[1], root[2], 
                       color=basin_colors[i % len(basin_colors)], 
                       s=400, edgecolors='black', marker='*', label=f"Stable Root {i+1}")

        # 5. Get and Plot Saddle Points (The Tipping Points)
        all_roots, types = self.find_eq_points()
        saddles = all_roots[["Saddle" in t for t in types]]
        
        if len(saddles) > 0:
            ax.scatter(saddles[:,0], saddles[:,1], saddles[:,2], 
                       color='blue', s=150, edgecolors='white', 
                       marker='D', label="Saddle Point (Tipping Point)")

        # Formatting
        ax.set_xlabel('Coral (C)')
        ax.set_ylabel('Turf (T)')
        ax.set_zlabel('Macroalgae (M)')
        ax.set_title("Full Ecological Landscape: Basins & Tipping Points")
        ax.view_init(elev=30, azim=45)
        ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1))
        
        plt.tight_layout()
        plt.show()
        print(volumes)

        
    def set_parameters(self, new_params=None, **kwargs):
        """
        Update parameters via a dictionary or keyword arguments.
        Usage: 
            model.set_parameters({'rc': 0.8})
            model.set_parameters(rc=0.8, theta=0.2)
        """
        # Combine dictionary and keyword arguments
        # note keyword arguments "win"
        updates = new_params if isinstance(new_params, dict) else {}
        updates.update(kwargs)

        # now update
        for key, value in updates.items():
            if hasattr(self.p, key):
                # check value:
                if not self.parameter_range[key][0] <= value <= self.parameter_range[key][1]:
                    print(f"Warning: Parameter '{key}' has a value outside the range. \
                            Setting anyway")
                setattr(self.p, key, value)
            else:
                print(f"Warning: Parameter '{key}' not found in model.")

    def get_output(self):
        """
        Return the output from the model
        """
        return self.output

from types import SimpleNamespace

class Mumby(CoralODELab):

    def __init__(self):
        super().__init__("Mumby")
        self.num_parameters = 5
        self.num_eq = 2
        self.parameters = {
                "a": 0.1,
                "g": 0.3,
                "y": 0.77,
                "r": 0.55,
                "d": 0.24
                }
        self.p = SimpleNamespace(**self.parameters)        
        self.parameter_names = {
                "a": "overgrowth",
                "g": "grazing",
                "y": "growth rate, algae",
                "r": "recruitment, coral",
                "d": "mortatility, coral"
                }
        self.parameter_range = {
                "a": [0.01, 0.5],
                "g": [0.001, 0.5],
                "y": [0.1, 1],
                "r": [0.1, 0.9],
                "d": [0.01, 0.5]
                }
        self.citation = "Mumby, P.J., Hastings, A. and Edwards, H.J. (2007), Thresholds and the resilience of Caribbean coral reefs, Nature, Vol. 450 No. 7166, pp. 98–101."
    
    def ode(self, z, t):
        r"""
        Setting up the equations from Mumby et al. 2007 for turf, coral and macroalgae
        ..math::
        Turf = T
        Coral: \frac{dC}{dt} = \underbrace{rTC}_{recruitment \, growth} - \underbrace{dC}_{mortality} - \underbrace{\alpha MC}_{overgrowth\, by \,M}
        
        Macroalgae: \frac{dM}{dt} = \underbrace{\alpha MC}_{M \, overgrows \, C} - \underbrace{\frac{gM}{M+T}}_{grazed \, M \, becomes \, T} + \underbrace{\gamma MT}_{M \, spreads \, over \, T}
       
       
           """
        T = 1 - sum(z)
        C = z[0]
        M = z[1]
         
        #coral
        recruitmentC = self.p.r * T * C
        mortalityC = self.p.d * C
        overgrowth = self.p.a * M * C
        dCdt = recruitmentC - mortalityC - overgrowth
        
        # macroalgae
        Movergrowth = self.p.a * M * C
        grazing = (self.p.g * M) / (M + T)
        growth = self.p.y * M * T
        dMdt = Movergrowth - grazing + growth
        
    
        return[dCdt, dMdt]
    
    def analytical_jacobian(self, z, t=0):
        """
        Analytical Jacobian matrix [ [d(dCdt)/dC, d(dCdt)/dM],
                                     [d(dMdt)/dC, d(dMdt)/dM] ]
        allows for calculating of equilbrium and makes the plots
        easier
        
        """
        C = z[0]
        M = z[1]
        T = 1 - C - M
        
        #partial derivative of dC/dt
        
        #change of dC/dt as coral chsnges
        recruitmentdC = self.p.r *(1 - 2 * C - M)
        mortalitydC = self.p.d
        overgrowthdC = self.p.a * M
        dCdC = recruitmentdC - mortalitydC - overgrowthdC
        
        #change of dC/dt as macroalagae changes
        recruitmentdCM = -self.p.r * C
        overgrowthdCM = self.p.a * C
        dCdM = recruitmentdCM - overgrowthdCM
       
        #partial derovative of dM/dt
        
        #change of dM/dt as coral changes
        MovergrowthdM = self.p.a * C
        grazingdM =self.p.g / (1 - C)
        growthdM = self.p.y * (1 - C - (2 * M))
        dMdC = MovergrowthdM + growthdM - grazingdM
        
        #change of dM/dt as macroalgae changes
        MovergrowthdMM = self.p.a * C
        GrowthdMM = self.p.y * (1 - C - 2 * M)
        grazingdMM = self.p.g / T
        dMdM = MovergrowthdMM + GrowthdMM - grazingdMM

        return np.aray([[dCdC, dCdM],
                        [dMdC, dMdM]])
    
if __name__ == "__main__":
    #set up inital conditions for the bifurcation plot
    model = Mumby()
    model.set_start_conditions([0.5,0.1])
    model.solve_time()
    model.plot_through_time()
    model.plot_bifurcation(parameter= "g")
    model.plot_phase_space(grid_density=8, t_end=100)
        

