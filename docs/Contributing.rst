Contributing to PYME
********************

We welcome contributions of bug reports, new features, bug fixes, and especially documentation. The process is similar to contributing
to other open source projects - in general your patch is likely to face robust criticism, comments, and requests for change
or justification. None of this should be taken personally and this does not mean that your contribution is not valued.
Patches may take some time to be reviewed, as this takes place during the gaps in a busy academic schedule. In general I
aim to provide some feedback within a week of a PR or issue being submitted, but this will not always happen, particularly
around grant submission deadlines etc ... It's entirely possible that a PR might get lost in noise - if you haven't heard
**anything** in a couple of weeks, don't be afraid to comment on the PR to bump it back into my attention.

When considering adding a feature, or re-working parts of the code please reach out in advance,
either by email, or by raising a feature request or proposal issue in our issue tracker. This will both serve to head off
potential points for friction (see below), and should also allow us to provide additional information which may be helpful
when dealing with some of the hairier and less well documented bits of the codebase.

Versioning and Releases
=======================

PYME operates a "continuous alpha" release model where we try and get changes into the head as soon as possible. This
means that there will inevitably be some regressions, but we do endeavour to ensure backwards compatibility. Whilst
feature development often occurs in separate branches, we do not have formal staged, 'stable', releases. The reasoning
behind this is that we are still a relatively small project, with a small team of core developers and want to get new
features out as soon as we can. In line with this continuous alpha model, we use date based versioning (we also record
the last commit hash for sub-day versioning). The current version of PYME is thus always the date of the last commit to
the master branch. In theory, `PYME.version.version` should track this but it can lag due to how `PYME.version.version` is
updated (see issue #312).

In addition, we have tagged "releases" corresponding to the the generation of conda and pip packages (and hopefully, as
we improve CI, executable installers). These "releases" do not imply that the code is any better / more stable than that
in the repository head - they simply mark when packages were built. Package building is currently manually triggered, but
this will hopefully change to an automated weekly build in the near future.

Roadmap / Future directions
===========================

**PYME is a moving target**. It has grown to be a rather large project with a huge number of dependencies. This is starting to make maintenance
time consuming and makes it hard to quickly merge new functionality. We intend to split the project into a GUI
independent core, and have the various GUIs interface with this. We also envisage splitting off some of the functionally
distinct modules. The exact restructuring has yet to be decided, but at this point we encourage separation of GUI and
logic to the extent possible. To facilitate this separation, we strongly suggest that new processing functionality for
either `dh5view` or `VisGUI` be implemented in the form of 'recipe' modules using `traits` to define parameters.

Python 3 Migration
==================

Python 3 migration is now mostly complete, although there are still a few corners of the code base and a couple of dependencies
which might have issues. For that reason we will continue to support python 2.7 until at least the end of 2020. As a result,
contributions should be written to be compatible with both python 2.7 and python 3.6, using modules such as six where appropriate.

Coding style
============

The coding style in PYME as it stands is fairly inconsistent. I'd like to improve on this. New code should:

- follow PEP8 where possible
- use Numpy style docstrings
- have strong model-view separation
- be written so as to be compatible with both python 2.7 and python > 3.6.

This **DOES NOT** mean that changes to existing variable names to follow PEP8 are welcome. Changes to existing variable
names incurs a significant proof-reading cost for very little benefit, adding significant "noise" to pull requests. A
personal aesthetic preference for a particular style does not justify changes to otherwise functioning code. The
exception here is classes and functions which form part of our "API" (i.e. might be called from user code / new code)
where a good case can be made for conversion to PEP8 in order to present a consistent interface. The bar for such API
changes however is high in order not to break existing code. Such changes:

- Should be discussed in advance (both to identify areas - potentially in projects other than the core PYME - where the API is
  used and also to decide if further refactoring / changes to the API should occur at the same time. There are multiple
  places in PYME where the API has evolved and might no longer be the most logical way of calling things. If we are
  putting the effort into changing all our calls, we might as well get the API right at the same time.)
- Should be in a separate PR which only deals with re-naming
- Must consider how the code might be used (e.g. several people use bits of PYME from ipython notebooks) and provide
  backwards compatible fallbacks (along with deprecation warnings) where appropriate

Documentation
=============

In addition to providing Numpy-style docstrings for any new code submitted, any effort to improve the existing documentation is 
extremely welcome. Our documentation needs to cater to two distinct audiences - *"end users"* who are often biologists and 
may not have any exposure to coding (or even running stuff on the command line), and *"developers"* who wish to
create plugins, use some of our library code, or contribute back to PYME. In general, documentation can fall into one of 
four categories: a tutorial, a how-to guide, an explanation, or a reference. We are not prescriptive about how documentation
should be written, but the Divio documentation system (https://documentation.divio.com/) is a good inspiration for what makes 
good documentation. 

**Writing documentation is a great way to get involved**, even if you are not an expert coder. If you had difficulty getting something 
to work, but then found a solution, **please write it up** and submit! If coding as `.rst` is a bit scary, you can 
also submit documentation by opening a feature request and attaching a .docx or .pdf. Documentation submitted this way may take several
months before we manage to re-format it, but is still immensely valuable (we'll make it available as .pdf in the interim).

Licensing
=========

PYME is licenced as GPLv3. By submitting a PR you acknowledge that you are happy (and have approval if necessary) for
your submitted code to be released under that license. We additionally want to keep the option of releasing parts of PYME
under a more permissive BSD license in the future. If you are not willing for your submitted code to be re-licensed as BSD
you must indicate this in your PR, and in comments in your code.


Pull requests
=============

Pull requests are always welcomed, but to increase the chances of speedy review and incorporation should:

- Address a single, fairly narrowly defined issue.
- Clearly identify if they are a bug fix or new functionality.
- Provide some context about what part(s) of the code are affected.
- Describe what the problem was, and why this is the best solution (I might ultimately disagree, but knowing the
  intent is really useful).

Pull requests which change existing variable names for the hell of it (see above) are likely to be rejected even if they
include useful new functionality or bugfixes as the maintenance burden of such changes is high.

When to include code in PYME and when to write an extension module?
===================================================================

PYME now has a reasonably usable plugin system by which modules for VisGUI, dh5view, and recipes can live outside the
main repository and yet still be discovered and used by the core components. Developing plugins outside of the core
repository has the advantage that you don't need to wait on me, and also helps keep the overall codebase more
comprehensible. My suggestions are thus:

- If the new functionality can stand alone and only uses established plugin interfaces it is likely to be easier to
  develop outside the core codebase, at least initially. Should this be something of wider interest moving it to the
  core can be done at a later stage.
- If the new functionality requires modification to any of the core components, it should either be developed within
  the PYME codebase, or split into the development of a new interface within the core code, and a standalone component.
- I want to discourage long lasting 'forks' - i.e. if it affects the core, we should hopefully be able to merge
  relatively quickly so everyone is using the same core.
- One potentially attractive option would be to have an official 'PYME-plugins' repository which put plugins in a place
  where they can get easily distributed, but which could have substantially laxer stringency on what we accept.

Regardless of the approach taken, I'm keen to be involved as early in the process as possible.
