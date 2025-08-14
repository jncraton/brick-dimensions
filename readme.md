# brick-dimensions

Calculate the dimensions of LEGO bricks from LDraw models

[<img width="512" height="256" alt="image" src="https://github.com/user-attachments/assets/6426f353-5a53-484a-84c7-4a1b39e68bd3" />](https://commons.wikimedia.org/wiki/File:Lego_dimensions.svg)

## Generated Output

This project generates a csv file with dimensions for all Rebrickable parts that have a valid LDraw part with the same part number.

Here's an example of the generated output:

| part_num | width | length | height |
|----------|-------|--------|--------|
| 3005     | 0.8   | 0.8    | 1.12   |
| 3010     | 0.8   | 3.2    | 1.12   |
| 3029     | 3.2   | 9.6    | 0.48   |

The complete [brick-dimensions.csv file](https://jncraton.github.io/brick-dimensions/brick-dimensions.csv) is available for direct download.

## Validation

Several parts have been spot-checked against Bricklink part dimensions, and a number of parts are automatically validated by unit tests.

## Building Locally

This project has only been tested on Debian-based Linux. In order to run this program, you will need the LDraw parts library. It is expected that this lives in `ldraw` and can be installed as `ldraw-parts`, though this will not include the most recent part updates.
