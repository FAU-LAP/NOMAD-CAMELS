# Interpolation with Floating-point Numbers

This Documentation will explain how to interpolate Floating-point Numbers with Breakpoint Tables.

## The Problem
Interpolation is a type of Linearization that uses the `RVAL` field of a record with which to interpolate.
The `RVAL` field can only be a `LONG` value, i.e. integers. Floating-point Numbers are however `DOUBLE` values and are only saved in the `VAL` field, the `RVAL` value stays `0`. No Interpolation is performed.
<br>
The workaround of simply forcing a `DOUBLE` value into the `RVAL` field, e.g. by writing it directly into the `RVAL` field, will lose all decimal digits, therefor lose accuracy.

## The Solution
To circumvent this, an intermediate output record is needed to scale the value. This record will do the following:
1. gets the value of a record that has the value with which to interpolate.
2. multiplies it by a factor of 10<sup>n</sup>, `n` depending of the needed accuracy, i.e. decimal digits needed (for this example, `n` will be 3).
3. writes the new value to the `RVAL` field of a record which then interpolates with that breakpoint table.

To give an example, lets say a tank fill level is calculated in millimeters with three decimal digits and needs to be interpolated to get a fill level in liters. This record gets that fill level in mm written into by a calcout record. Note that since all records here are `Passive`, the calcout record should force the scaling record to process, for example via the `FLNK` field.

```
record(ai, FillLevel:filllevelMM)
{
	field (DESC, "Fill level of a helium tank in mm")
	field (DTYP, "Soft Channel")
	field (SCAN, "Passive")
	field (EGU, "mm")
}
```

The scaling record is an analog output record, that should look like this:
```
record(ao, FillLevel:scaling)
{
	field (DTYP, "Raw Soft Channel")
	field (OMSL, "closed_loop")
	field (SCAN, "Passive")
	field (OIF, "Full")
	field (DOL, "FillLevel:filllevelMM.VAL")
	field (OUT, "FillLevel:filllevelL.RVAL PP")
	field (LINR, "LINEAR")
	field (ASLO, 0.001)
}
```
* `DTYP` needs to be `Raw Soft Channel`, so the `RVAL` value is written to the record in the `OUT` field.
* `OMSL` set to `closed_loop` enables the input field `DOL`.
* `OIF` is set to `Full` because otherwise the `VAL` field is incremented and not used as a new value.
* `DOL` is where the value is taken from.
* `OUT` is where is written to. Its important to write to the `RVAL` field to enable interpolation in the target record. The `PP` flag is set to process the receiving record.
* `LINR` needs to be set so `ASLO` is used.
* `ASLO` is set to 10<sup>-3</sup>. This is because the way this record works is by reading the field specified by the `DOL` field and saving that value in its `VAL` field. Then, due to being a `Raw Soft Channel`, calculates the outgoing `RVAL`. Since `VAL = RVAL * ASLO`, `RVAL = VAL / ASLO`.
<br>

The receiving record then can interpolate with a breakpoint table, in this example a custom one called `filllevel`.
```
record(ai, FillLevel:filllevelL)
{
	field (DESC, "Filllevel of the Heliumtank in L")
	field (DTYP, "Raw Soft Channel")
	field (SCAN, "Passive")
	field (LINR, "filllevel")
	field (EGU, "l")
}
```
* `LINR` set to `filllevel` tells the record to use the breakpoint table `filllevel`
* `DTYP` needs to be `Raw Soft Channel` again to use `RVAL`.

Due to the `input` value of the breakpoint table now being scaled up by a factor of 10<sup>3</sup>, the breakpoint table also needs to be adjusted by this factor.
For this example, while the (abbreviated) original breakpoint table looked like this:
```
breaktable(filllevel) {	
	0.0	0.0
	10.0	1.0
	20.0	3.0
	30.0	6.0
...
...
	1470.0	4231.0
	1480.0	4237.0
	1487.0	4239.8
}
```

It now has to be scaled to look like this:

```
breaktable(filllevel) {
	0.0     	0.0
	10000.0		1.0
	20000.0		3.0
	30000.0		6.0
...
...
	1470000.0	4231.0
	1480000.0	4237.0
	1487000.0	4239.8
}
```