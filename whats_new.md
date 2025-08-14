## Latest Release Notes
pyGCodeDecode has gotten several updates which are now published with Version XX.XX.
These include QOL improvements and error fixes.

### Result Calculation
A separate result calculation module is added, which is executed after simulation. User defined results may be calculated using the resulting trajectory and can be mapped to the segments. See current implementations for details.

### Plotting updates
Plotting methods are moved to be separated from the simulation objects. They now allow for several arguments to be passed to the `pyvista` visualization toolkit. The scalar value plotted may be selected via keys, allowing different results to be displayed. Further individual layer plotting is supported, if a layer cue is provided. Additional arguments enable advanced settings such as transparent background, lighting and rendering options. This includes camera position and orientation.
Further, the plotting methods allow a callable to be passed; the user may modify the `pyvista`-scene through these and add geometry to the plot.
Screenshots are also improved visually by wrapping the pyvista screenshot into a `matplotlib` axis, which allows for nicer colorbars and vector graphics rendering of text.
Individual extrusions now are represented through a squiched cylinder instead of a circular one. This squiching can be set by the user and results from the layer width to height ratio.

### Junction Handling Bug fixes
Several bug fixes are implemented for junction handling, improving the overall robustness of the simulation and ensuring accurate results. The firmware identifiers have been changed to be more consistent.

### Prints
Print statements have been improved for better clarity and information. A verbosity control is added to declutter the output, especially when running a large number of simulations. They now include more context about the simulation state and results, making it easier to understand the output. Consistent formatting and different verbosity levels are supported.

### Testing and Type Hints
More tests have been added to ensure a reliable simulation and framework. Especially the junction handling module is tested more thoroughly.
More type hints have been added throughout the codebase to improve readability and facilitate easier debugging and development. Physical quantities are morphed by mathematical operations to yield the correct units, allowing for more intuitive code and reducing the likelihood of errors.
