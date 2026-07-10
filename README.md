# Beautyofvisuals

Python Manim projects for educational explainer videos.

## Repository layout

- `requirements.txt`: shared dependency base for every project folder.
- `render.ps1`: root PowerShell entrypoint that can run any project folder.
- `MOI/`: self-contained Moment of Inertia animation project.
- `MOI/main.py`: the Manim scene definitions.
- `MOI/README.md`: project-specific setup and render instructions.
- `MOI/requirements.txt`: project-specific dependency wrapper.
- `MOI/render.ps1`: project-local PowerShell render helper.

Generated files such as Manim media output, caches, and local virtual environments are intentionally ignored.
Each animation project keeps its code and generated videos in the same project folder.
To add a new project, create another sibling folder like `MOI/` with `main.py`, `requirements.txt`, `render.ps1`, and `media/`.
The root scripts are set up so more project folders can be added without changing the top-level layout.

## Quick start

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
.\render.ps1 -Project MOI -Scene SpinnerIntuition -Preview
```

## Current project

`MOI` contains a full moment of inertia explainer made of these scenes:

1. `SpinnerIntuition`
2. `RotationalNewton`
3. `MomentDefinition`
4. `ParallelAxisTheorem`
5. `PerpendicularAxisTheorem`
6. `RingCentralAxis`
7. `RingAllAxes`

For detailed setup notes, output locations, and direct Manim commands, see [MOI/README.md](MOI/README.md).

## Structure rule

Each video project should follow this pattern:

- `ProjectName/main.py`: Manim scenes for that project
- `ProjectName/requirements.txt`: project dependencies
- `ProjectName/render.ps1`: project render helper
- `ProjectName/media/`: generated Manim output for that project only

That keeps source code and rendered video assets grouped together instead of mixing outputs across projects.
