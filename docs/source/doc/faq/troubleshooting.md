# Troubleshooting

## General Hints
Sometimes packages that CAMELS depends have specific versions that do not work for CAMELS, although they lie within the specified version-range.

To fix such issues try running the following in your CAMELS python environment:
```
pip install --upgrade nomad-camels --upgrade-strategy eager
```

Please [contact us](../../contact.md) if it still does not work!

## Instrument not recognized

When CAMELS does not recognize your instrument being connected, this may come from missing libraries on your computer.

A common case is that specific VISA libraries are needed, for this you may need to install [Keysight-VISA](https://www.keysight.com/de/de/lib/software-detail/computer-software/io-libraries-suite-downloads-2175637.html) or [NI-VISA](https://www.ni.com/de/support/downloads/drivers/download.ni-visa.html#558610).

Some instruments need specific libraries provided by the vendor. If that is the case, most CAMELS drivers provide a link to the vendor's website on their [PyPI-page](https://pypi.org/).
