<div style="height: 90pt;"></div>
<div style="flex: 0 0 8%; margin-top: -10pt;">
<img src="oxford-logo.png">
</div>
<div style="flex: 0 0 65%; text-align: center;">
<h1 style="margin-bottom: 10pt;">Diffrax: JAX-based numerical differential equation solvers</h1>
<h2>Patrick Kidger</h2>
</div>
<div style="flex: 1">
    <div style="display: flex; align-items: center;">
        <img style="height: 20pt; width: 20pt; margin: 5pt;" src="icons/fontawesome/brands/github.svg">
        <div style="font-size: 0.9rem; margin-right: 5pt;"><a href="https://github.com/patrick-kidger/diffrax">github.com/patrick-kidger/diffrax</a></div>
    </div>
    <div style="display: flex; align-items: center;">
        <img style="height: 20pt; width: 20pt; margin: 5pt;" src="icons/fontawesome/brands/twitter.svg">
        <div style="font-size: 0.9rem;"><a href="https://twitter.com/PatrickKidger">@PatrickKidger</a></div>
    </div>
</div>

--split--

!!! abstract "Summary of features"

    - Ordinary/stochastic/controlled diffeq solvers;
    - High-order, implicit, symplectic solvers;
    - Using a PyTree as the state;
    - Dense solutions;
    - Multiple adjoint methods for backpropagation.

## Easy-to-use syntax

Let's solve the ODE \\(\frac{\mathrm{d}y}{\mathrm{d}t} = -y\\):

```python
from diffrax import diffeqsolve, ODETerm, Dopri5
import jax.numpy as jnp

def f(t, y, args):
    return -y

term = ODETerm(f)
solver = Dopri5()
solution = diffeqsolve(term, solver, t0=0, t1=1, dt0=0.1,
                       y0=jnp.array([2., 3.]))
```

## New idea: unified solving

At a technical level, the internal structure of the library does some pretty cool new stuff! Most important is the idea of solving ODEs and SDEs in a single unified way; this produces a small tightly-written library.

Specifically: ordinary differential equations
\\[\frac{\mathrm{d}y}{\mathrm{d}t} = f(t, y(t))\\]
and stochastic differential equations
\\[\mathrm{d}y(t) = f_1(t, y(t))\,\mathrm{d}t + f_2(t, y(t))\,\mathrm{d}w(t)\\]
are solved in a unified way by lowering them to *controlled* diffeqs:
\\[\mathrm{d}y(t) = f(t, y(t)) \,\mathrm{d}x(t).\\]
where e.g. \\(x(t) = t\\) for an ODE and \\(x(t) = [t, w(t)]\\) for an SDE.

--split--

## Versus other libraries?<br>(torchdiffeq, Julia etc.)

Diffrax is better for advanced use cases:

- Adding your own custom ops;
- Solving ODEs/SDEs simultaneously;
- Solving SDEs with controls, or multiple noise terms.
- etc.

Diffrax is also *fast*.

- 1.3--20 times faster than torchdiffeq.
- Similar speed to DifferentialEquations.jl (precise benchmarks WIP).

## Extending Diffrax

Diffrax is designed to be highly extensible.

- There are a sophisticated collection of abstract base classes (`AbstractSolver` etc.) through which you can easily add custom ops.

- If you're writing e.g. a differentiable simulator and want to step through the solve yourself, then this is also possible.

!!! tip "Next steps"

    **Installation:** `pip install diffrax`<br>
    **Documentation:** [https://docs.kidger.site/diffrax](https://docs.kidger.site/diffrax)<br>
    <div style="display: flex; margin-top: -10pt;">
    <div style="flex: 1">**Reference:**&nbsp;</div><div style="flex: 100;">P. Kidger, *On Neural Differential Equations*, Doctoral Thesis, University of Oxford 2021</div>
    </div>
    <div style="margin-top: -10pt;">
    ```bibtex
    @phdthesis{kidger2021on,
        title={{O}n {N}eural {D}ifferential
               {E}quations},
        author={Patrick Kidger},
        year={2021},
        school={University of Oxford},
    }
    ```
    </div>
