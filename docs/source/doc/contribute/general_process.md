# Welcome to CAMELS Guide for Contributing

Thank you for investing your time in contributing to our project!

Read our [Code of Conduct](code_of_conduct.md) to keep our community approachable and respectable.

## Create a new issue

If you spot a problem with CAMELS, search if an issue already exists. If a related issue doesn't exist, you can open a new issue using a relevant [issue form](https://github.com/FAU-LAP/NOMAD-CAMELS/issues).

## Make Changes

There are two ways in which you can contribute to the CAMELS project.

### 1. Add New Instrument Drivers

If you have developed a new instrument driver for CAMELS, it can be easily added to the existing instrument drivers in our [driver repository](https://github.com/FAU-LAP/CAMELS_drivers/tree/development).

1. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo#fork-an-example-repository) the [development branch](https://github.com/FAU-LAP/CAMELS_drivers/tree/development) of our repository.
2. Create a working branch and start with your changes!
3. Make modifications to the repository, like adding a new instrument driver or improving an existing one.
4. Commit the changes once you are happy with them. Keep in mind to name your commits in an understandable way as this makes reviewing your code much easier.
5. When you're finished with the changes, create a pull request.
6. Don't forget to [link](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) your PR to an issue if you are solving one.
7. The CAMELS development team will then review your pull request and may ask for changes to be made before a PR can be merged. You can apply suggested changes directly through the UI. You can make any other changes in your fork, then commit them to your branch.

### 2. Modify the CAMELS Source Code

Any one can help make CAMELS better by adding new functionality or improving existing code.

1. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo#fork-an-example-repository) the [development branch](https://github.com/FAU-LAP/NOMAD-CAMELS/tree/development) of our repository.
2. Create a working branch and start with your changes!
3. Make modifications to the repository, improving CAMELS.
4. Commit the changes once you are happy with them. Keep in mind to name your commits in an understandable way as this makes reviewing your code much easier.
5. When you're finished with the changes, create a pull request.
6. Don't forget to [link](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) your PR to an issue if you are solving one.
7. The CAMELS development team will then review your pull request and may ask for changes to be made before a PR can be merged. You can apply suggested changes directly through the UI. You can make any other changes in your fork, then commit them to your branch.

**If your contribution was successfully reviewed your pull request will be merged.** &#127881;

### Note about Branches

The most recent version of CAMELS and the CAMELS drivers can always be found in the _development_ branch. We will then update the main branches with the content of the development branches if they have been proven to run stably.

There are frequent updates of CAMELS and the CAMELS drivers to PyPI, so that you can simply `pip install` them.