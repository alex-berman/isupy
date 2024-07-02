`isupy` is a Python package for dialogue management based on information-state update (ISU). The package provides an approach for declaring a dialogue state and for declaring and invoking ISU rules.
This repository also contains an example application for a fairly basic slot-filling application.

# Status
The current version of the package supports automated testing using semantic expressions for dialogue moves. There is currently no built-in support for integrating `isupy` with other dialogue components such as natural-language understanding (NLU) and generation (NLG).

# Example
The example application enables the user to make appointments. The application is dialogue-only; no actual appointments are made. For a repertoire of supported dialogue capabilities, see the [dialogue tests](examples/appointment/test/dialog_converage_sem.yml). To run the tests, execute:

```
pytest examples
```

# Requirements
Python 3.6 or later
