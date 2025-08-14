# brick-dimensions

Calculate the dimensions of LEGO bricks from LDraw models

## Generated Output

This project generates a csv file with dimensions for all Rebrickable parts that have a valid LDraw part with the same part number.

Here's an example of the generated output:

| part_num | width | length | height |
|----------|-------|--------|--------|
| 3005     | 0.8   | 0.8    | 1.12   |
| 3010     | 0.8   | 3.2    | 1.12   |
| 3029     | 3.2   | 9.6    | 0.48   |

Complete output can be found [here](https://jncraton.github.io/brick-dimensions/brick-dimensions.csv).

## Building Locally

This project has only been tested on Debian-based Linux. In order to run this program, you will need the LDraw parts library. It is expected that this lives in `/usr/share/ldraw` and can be installed as `ldraw-parts`, though this will not include the most recent part updates.
