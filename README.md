## CSM Undergraduate Research Fellowship

This repository documents the research work that I did for my CSM Undergraduate Research Fellowship. The goal of this project was to improve the performance of [Faial](https://gitlab.com/umb-svl/faial) by optimizing [Z3 logic selection](https://microsoft.github.io/z3guide/docs/logic/intro/).

## User Manual

1. Install Faial from the [project repositority](https://gitlab.com/umb-svl/faial).
2. Open a console window.
3. run ``git clone https://github.com/pyreking/csm-fellowship.git`` to clone this repository.
4. run ``cd csm-fellowship`` to go to the project directory.
5. run ``python src/run.py`` to benchmark Faial using different Z3 logics.
6. Edit ``plot.py`` to call ``plot_file_id_and_elapsed_time()``, ``plot_mean_median_std()``, ``plot_status()``, or ``plot_consistency()``.
7. run ``python src/plot.py`` to view the graph.

## Figures
Go to ``csm-fellowship/Figures`` to see all the figures that were created for this research project.

## Acknowledgements

The work of AG was supported in part by College of Science and Mathematics Dean’s Undergraduate Research Fellowship through fellowship support from Oracle, project ID R20000000025727.

This material is based upon work supported by the National Science Foundation under Grant No. 2204986.

This work was supported in collaboration with the [Software Verification Lab](https://umb-svl.gitlab.io/).
