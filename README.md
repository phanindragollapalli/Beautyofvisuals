# Beautyofvisuals

This repository contains the Python Manim code used to create visual explainer videos.

## MOI Folder

The `MOI` folder is a self-contained Manim project focused on moment of inertia. It is built around one main animation script and a few supporting files that make it easy to run and render the video locally.

At a high level, the folder includes:

- `main.py`: the core Manim script containing the full sequence of scenes.
- `requirements.txt`: the Python dependencies and quick setup or render commands.
- `prompt.md`: short project notes and direction for the video.
- `media/`: rendered outputs and other generated assets created by Manim.

## What The Script Covers

`main.py` contains 7 scenes, and together they build the explanation for the video from intuition to formal results:

- `SpinnerIntuition`: introduces the main idea using two wheels with the same mass but different radii.
- `RotationalNewton`: connects torque and angular acceleration to show why rotational motion changes differently.
- `MomentDefinition`: introduces the actual moment of inertia definition.
- `ParallelAxisTheorem`: explains how shifting the axis changes the moment of inertia.
- `PerpendicularAxisTheorem`: shows the perpendicular axis relationship for flat objects.
- `RingCentralAxis`: looks at a ring about its central axis.
- `RingAllAxes`: compares the ring across multiple axes for a fuller geometric view.

## How To Run

From inside the `MOI` folder:

1. Create and activate a virtual environment.
2. Install the Python dependencies with `pip install -r requirements.txt`.
3. Render a scene with a command like `manim -pqh main.py SpinnerIntuition`.

The same pattern works for the other scene names listed above.
