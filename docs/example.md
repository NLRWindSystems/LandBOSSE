# User Guide

This example will work with the `project_input_template/project_list_simplified.xlsx`, which
includes the GE 1.5 MW validation example (`project_input_template/project_data/ge15_public.xlsx`).
Using these data, we will walk through the setup of the project-specific data, project listings,
and running the model.

## Project Input Data

LandBOSSE relies on the use of separate input and output folders. For any set of projects, these
can be defined as environment variables using the names `LANDBOSSE_INPUT_DIR` and
`LANDBOSSE_OUTPUT_DIR`, or provided when running the code (more details in [Running LandBOSSE](#running-landbosse)).

An example of a project input folder is provided with the code: the folder `project_input_template/`
where listings of projects can be stored and the subfolder `project_data` where all project-specific
Excel files are stored.

### Project listing and the `LandBOSSERunner` API

As stated in the introduction, we'll be working with `project_list_simplified.xlsx` which contains
a single project (unlike `project_list.xlsx` which runs several projects simultaneously), the
public-facing GE 1.5 MW example (`ge15_public.xlsx`).

The below table explains each of the expected parameters found when setting up either the
`project_list.xlsx` or the `LandBOSSERunner` input dictionary. For Excel setups, each row in
"Project List Column" represents a column name in the project list Excel file. Using the Excel setup,
we can run multiple projects, though this example relies models a single project. Similarly, using
the `LandBOSSERunner` configuration dictionary, each row in "LandBOSSE Runner Key" represents a
dictionary key. Notably, using the `LandBOSSERunner` API enables single project runs only. In both
cases the "Description" column describes what data are expected as an Excel sheet's cell value or
dictionary key's value.

| Project List Column                                                  | LandBOSSE Runner Key                            | Description                                                                                                                                     |
| -------------------------------------------------------------------- | ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Project ID                                                           | id                                              | Name of the project                                                                                                                             |
| Project data file                                                    | data_tables                                     | Excel filename associated with the project                                                                                                      |
| Total project construction time (months)                             | construction_months                             | Total construction duration (months)                                                                                                            |
| Turbine rating MW                                                    | turbine_rating_MW                               | Capacity of turbine (MW)                                                                                                                        |
| Hub height m                                                         | hub_height_m                                    | Turbine hub height (m)                                                                                                                          |
| Rotor diameter m                                                     | rotor_diameter_m                                | Turbine rotor diameter (m)                                                                                                                      |
| Turbine spacing (times rotor diameter)                               | turbine_spacing_rotor_diameter                  | Layout spacing between turbines in each row, in rotor diameters                                                                                 |
| Row spacing (times rotor diameter)                                   | row_spacing_rotor_diameter                      | Layout spacing between rows, in rotor diameters                                                                                                 |
| Number of turbines                                                   | num_turbines                                    | Number of turbines                                                                                                                              |
| Turbine Capex (USD/kW)                                               | turbine_capex                                   | CapEx of turbine ($/kW)                                                                                                                         |
| Breakpoint between base and topping (percent)                        | base_topping_breakpoint                         | Height at which cranes change from 'Base' to 'Topping', represented as a fraction of hub height                                                 |
| Fuel cost USD per gal                                                | fuel_cost_usd_per_gal                           | Cost of fuel per gallon ($/gal)                                                                                                                 |
| Rate of deliveries (turbines per week)                               | turbine_delivery_rate_per_week                  | Number of turbine deliveries (all components) per week                                                                                          |
| Wind shear exponent                                                  | wind_shear                                      | Wind shear (assumed constant across all timestamps and turbines)                                                                                |
| Foundation depth m                                                   | foundation_depth_m                              | Depth of concrete foundation (m)                                                                                                                |
| Rated Thrust (N)                                                     | rated_thrust_N                                  | Rated horizontal thrust of turbine (N)                                                                                                          |
| Bearing Pressure (n/m2)                                              | bearing_pressure_Pa                             | Bearing pressure capacity of soil underneath foundations (Pa)                                                                                   |
| 50-year Gust Velocity (m/s)                                          | gust_velocity_50_year_m/s                       | 50 year wind gust velocity (m/s)                                                                                                                |
| Line Frequency (Hz)                                                  | line_frequency                                  | Electrical frequency of grid (Hz)                                                                                                               |
| Combined homerun trench length to substation (km)                    | combined_homerun_trench_length_km               | Combined homerun trench length to substation (km) (optional - can be null but cannot be omitted)                                                |
| Non-Erection Wind Delay Critical Height (m)                          | non_erection_wind_delay_critical_height_m       | When calculating wind delays for non-erection tasks, shear values to this height (m)                                                            |
| Non-Erection Wind Delay Critical Speed (m/s)                         | non_erection_wind_delay_critical_wind_speed_m/s | When calculating wind delays for non-erection tasks, wind speeds above this value will force work to stop (m/s)                                 |
| Distance to interconnect (miles)                                     | distance_to_interconnect_mi                     | Distance from substation to switchyard (miles)                                                                                                  |
| Interconnect Voltage (kV)                                            | interconnect_voltage_kV                         | Voltage of grid (kV)                                                                                                                            |
| New Switchyard (y/n)                                                 | new_switchyard                                  | Should a new switchyard be built (true/false)                                                                                                   |
| Road length adder (m)                                                | road_length_adder_m                             | Distance from site entry point to the project (m)                                                                                               |
| Road Quality (0-1)                                                   | road_quality                                    | Non-dimensional representation of the quality of roads. 0 is poor quality, 1 is good quality. A higher road quality reduces the total road cost |
| Percent of roads that will be constructed                            | percent_roads_to_be_constructed                 | What percentage of roads need to be constructed vs already exist                                                                                |
| Road width (ft)                                                      | road_width_ft                                   | Width of roads (ft)                                                                                                                             |
| Road thickness (in)                                                  | road_thickness_in                               | Thickness of roads (in)                                                                                                                         |
| Calculate road cost for distributed wind? (y/n)                      | calculate_road_cost_for_distributed_wind        | Should road costs be included in the calculation for distributed wind projects (true/false)                                                     |
| Site prep area for Distributed wind (m2)                             | site_prep_area_for_distributed_wind_m2          | Site prep area for distributed wind projects (m^2)                                                                                              |
| Crane width (m)                                                      | crane_width_m                                   | Width of crane (m)                                                                                                                              |
| Number of highway permits                                            | num_highway_permits                             | Number of highway permits required                                                                                                              |
| Number of access roads                                               | num_access_roads                                | Number of site access roads required                                                                                                            |
| Overtime multiplier                                                  | overtime_multiplier                             | Labor cost multiplier for overtime work                                                                                                         |
| Allow same flag                                                      | allow_same_flag                                 | flag to indicate whether choosing same base and topping crane is allowed (true/false)                                                           |
| Override total management cost for distributed (0 does not override) | override_total_management_cost_for_distributed  | For distributed wind project, override the calculated management cost and use this value instead (0 means do not override)                      |
| Markup contingency                                                   | markup_contingency                              | Markup contingency                                                                                                                              |
| Markup warranty management                                           | markup_warranty_management                      | Markup warranty management                                                                                                                      |
| Markup sales and use tax                                             | markup_sales_and_use_tax                        | Markup sales and use tax                                                                                                                        |
| Markup overhead                                                      | markup_overhead                                 | Markup overhead                                                                                                                                 |
| Markup profit margin                                                 | markup_profit_margin                            | Markup profit margin                                                                                                                            |
| Utility Interconnection Fees (Small DW only)                         | utility_interconnection_fees_distributed_wind   | Fee for connecting to the grid (distributed wind projects only)                                                                                 |
| Labor cost multiplier                                                | labor_cost_multiplier                           | Multiplier to modify labor costs                                                                                                                |
| Crane breakdown fraction                                             | crane_breakdown_fraction                        | What fraction of cranes will breakdown. 0 means none, 1 means all. Breakdowns increase the total erection duration                              |
| No mapping available                                                 | enable_cost_and_scaling_modifications           | Should cost and scaling modifications be applied (true/false)                                                                                   |

### Project Excel Data

Regardless of how the above data are provided, an Excel file will be required for individual project
configurations. These data will contain various cost, logistics, site, and engineering data. Each
of the following subsections will show up to the first 10 rows of the data in `ge15_public.xlsx`
to demonstrate the data and formats required for the input data.

For each sheet below, except `weather_window`, additional columns can be provided after the listed,
required columns. These can be things such as notes and sources that are helpful for tracking
source data and any methodologies for transforming them to fit the LandBOSSE formats. In many
of the sheets in `ge15_public.xlsx`, there will be one or multiple notes and sources columns for
exactly this purpose. However, those data are not exemplified below.

#### `components`

- Component
- Mass tonne
- Lift height m
- Surface area sq m
- Coeff drag
- Coeff drag (installed)
- Section height m
- Lever arm m
- Cycle time installation hrs
- Offload hook height m
- Offload cycle time hrs
- Multplier drag rotor
- Multiplier tower drag

| Component         |   Mass tonne |   Lift height m |   Surface area sq m |   Coeff drag |   Coeff drag (installed) |   Section height m |   Lever arm m |   Cycle time installation hrs |   Offload hook height m |   Offload cycle time hrs |   Multplier drag rotor |   Multiplier tower drag |
|-------------------|--------------|-----------------|---------------------|--------------|--------------------------|--------------------|---------------|-------------------------------|-------------------------|--------------------------|------------------------|-------------------------|
| Nacelle GE 1.5SLE |         50   |              90 |               33    |          0.8 |                      0.8 |                  0 |            80 |                           1.5 |                       6 |                      0.5 |               1        |                       0 |
| Hub               |         15.4 |              90 |               11.3  |          1.1 |                      1.1 |                  0 |            80 |                           1   |                       6 |                      0.5 |               0        |                       0 |
| Blade 1           |          5.2 |              90 |               33.44 |          0.1 |                      1.4 |                  0 |            80 |                           1   |                       6 |                      0.5 |               0.666667 |                       0 |
| Blade 2           |          5.2 |              90 |               33.44 |          0.1 |                      1.4 |                  0 |            80 |                           1   |                       6 |                      0.5 |               0.666667 |                       0 |
| Blade 3           |          5.2 |              90 |               33.44 |          0.1 |                      1.4 |                  0 |            80 |                           1   |                       6 |                      0.5 |               0.666667 |                       0 |
| Tower section 1   |         59.8 |              30 |               95.89 |          0.6 |                      1.1 |                 25 |            12 |                           1   |                       6 |                      0.5 |               0        |                       1 |
| Tower section 2   |         39.3 |              60 |               96.25 |          0.6 |                      1.1 |                 25 |            37 |                           1   |                       6 |                      0.5 |               0        |                       1 |
| Tower section 3   |         30.9 |              90 |               90    |          0.6 |                      1.1 |                 30 |            65 |                           1   |                       6 |                      0.5 |               0        |                       1 |

#### `cable_specs`

- Array Cable
- Conductor Size (mm2)
- Current Capacity (A)
- Rated Voltage (V)
- AC Resistance (Ohms/km)
- Inductance (mH/km)
- Capacitance (nF/km)
- Cost (USD/LF)

| Array Cable   |   Conductor Size (mm2) |   Current Capacity (A) |   Rated Voltage (V) |   AC Resistance (Ohms/km) |   Inductance (mH/km) |   Capacitance (nF/km) |   Cost (USD/LF) |
|---------------|------------------------|------------------------|---------------------|---------------------------|----------------------|-----------------------|-----------------|
| AWG 1/0       |                    120 |                    300 |                  36 |                    0.253  |                0.398 |                 0.179 |               6 |
| AWG 4/0       |                    240 |                    440 |                  36 |                    0.125  |                0.359 |                 0.223 |               9 |
| MCM 500       |                    500 |                    640 |                  36 |                    0.0605 |                0.317 |                 0.293 |              13 |
| MCM1000       |                    800 |                    830 |                  36 |                    0.0367 |                0.291 |                 0.375 |              16 |
| MCM1250       |                   1000 |                    935 |                  36 |                    0.0291 |                0.284 |                 0.411 |              17 |

#### `equip`

- Equipment ID
- Operation
- Equipment name
- Crane capacity tonne
- Number of equipment

| Equipment ID   | Operation   | Equipment name   |   Crane capacity tonne |   Number of equipment |
|----------------|-------------|------------------|------------------------|-----------------------|
| E1             | Base        | Crawler crane    |                    500 |                     1 |
| E1             | Base        | Truck crane      |                     50 |                     1 |
| E1             | Top         | Crawler crane    |                    500 |                     1 |
| E1             | Top         | Truck crane      |                     50 |                     2 |
| E2             | Top         | Crawler crane    |                    600 |                     1 |
| E2             | Top         | Truck crane      |                     50 |                     2 |
| E2             | Top         | RT               |                    100 |                     2 |
| E3             | Top         | Crawler crane    |                    750 |                     1 |
| E3             | Top         | RT               |                    100 |                     2 |
| E4             | Top         | Crawler crane    |                   1000 |                     1 |
| ...            | ...         | ...              |                    ... |                   ... |

#### `crane_specs`

- Boom system
- Crane capacity tonne
- Speed of travel km per hr
- Hoist speed m per min
- Crew type ID
- Equipment ID
- Setup time hr
- Breakdown time hr
- Max wind speed m per s
- Hub height m
- Max capacity tonne
- Radius m
- Hook Height m
- Mobilization cost USD

| Equipment name   | Crane name   | Boom system      |   Crane capacity tonne |   Speed of travel km per hr |   Hoist speed m per min | Crew type ID   | Equipment ID   |   Setup time hr |   Breakdown time hr |   Max wind speed m per s |   Hub height m |   Max capacity tonne |   Radius m |   Hook Height m |   Mobilization cost USD |
|------------------|--------------|------------------|------------------------|-----------------------------|-------------------------|----------------|----------------|-----------------|---------------------|--------------------------|----------------|----------------------|------------|-----------------|-------------------------|
| Offload crane    | LB 75        | Hydraulic        |                     75 |                          40 |                      60 | C0             | OL1            |               0 |                   0 |                       10 |           12.5 |                   38 |        5.4 |            12.5 |                    8040 |
| Offload crane    | Big LB 2580  | Big Hydraulic    |                    500 |                          40 |                      60 | C0             | OL2            |               0 |                   0 |                       10 |           48   |                  500 |       11   |            48   |                  406100 |
| Offload crane    | LB 258       | Hydraulic        |                    200 |                          40 |                      60 | C0             | OL2            |               0 |                   0 |                       10 |           48   |                   63 |       11   |            48   |                   40610 |
| Crawler crane    | M999         | 22EL             |                    275 |                           2 |                      20 | C1             | B1             |               0 |                  40 |                        9 |           57   |                   67 |       14   |            57   |                   68709 |
| Crawler crane    | LR1500       | SL3F             |                    500 |                           2 |                      20 | C1             | E1             |               0 |                  40 |                        9 |           80   |                  102 |       16   |            94   |                  184398 |
| Crawler crane    | LR1500       | SL3F             |                    500 |                           2 |                      20 | C1             | E1             |               0 |                  40 |                        9 |           85   |                   95 |       16   |           100   |                  184398 |
| Crawler crane    | LR1500       | SL3F             |                    500 |                           2 |                      20 | C1             | E1             |               0 |                  40 |                        9 |           90   |                   87 |       16   |           106   |                  184398 |
| Crawler crane    | LR1500       | SL3F             |                    500 |                           2 |                      20 | C1             | E1             |               0 |                  40 |                        9 |          100   |                   77 |       18   |           112   |                  184398 |
| Crawler crane    | LR1500       | SL4DFB + Derrick |                    500 |                           2 |                      20 | C1             | E1             |               2 |                  40 |                        9 |           80   |                  112 |       16   |            94   |                  184398 |
| Crawler crane    | LR1500       | SL4DFB + Derrick |                    500 |                           2 |                      20 | C1             | E1             |               2 |                  40 |                        9 |           90   |                  105 |       16   |           100   |                  184398 |
| ...              | ...          | ...              |                    ... |                         ... |                     ... | ...            | ...            |             ... |                 ... |                      ... |          ...   |                  ... |      ...   |           ...   |                     ... |

#### `development`

- Type of cost
- Cost USD
- Phase of construction

|     Type of cost |   Cost USD |   Phase of construction |
|------------------|------------|-------------------------|
| Equipment rental | 0          | Development             |
| Labor            | 1000000    | Development             |
| Materials        | 0          | Development             |
| Mobilization     | 0          | Development             |
| Other            | 0          | Development             |

#### `crew_price`

- Labor type ID
- Hourly rate USD per hour
- Per diem USD per day

|        Labor type ID |   Hourly rate USD per hour |   Per diem USD per day |
|----------------------|----------------------------|------------------------|
| Crane operator       | 81.9105                    | 149                    |
| Oiler                | 61.625                     | 149                    |
| Rigger               | 85.84                      | 149                    |
| Truck driver         | 66.41                      | 149                    |
| Iron worker          | 94.5545                    | 149                    |
| Project manager      | 119                        | 149                    |
| Site manager         | 112.2                      | 149                    |
| Construction manager | 112.2                      | 149                    |
| Project engineer     | 93.5                       | 149                    |
| Safety or qc manager | 106.118                    | 149                    |
| ...                  | ...                        | ...                    |

#### `crew`

- Crew type ID
- Operation
- Crew name
- Labor type ID
- Number of workers

|   Crew type ID |             Operation |                      Crew name | Labor type ID        |   Number of workers |
|----------------|-----------------------|--------------------------------|----------------------|---------------------|
| M0             | Management            | Management - project size      | Project manager      |                   1 |
| M0             | Management            | Management - project size      | Site manager         |                   1 |
| M0             | Management            | Management - project size      | Construction manager |                   1 |
| M0             | Management            | Management - project size      | Project engineer     |                   1 |
| M0             | Management            | Management - project size      | Safety or qc manager |                   1 |
| M0             | Management            | Management - project size      | Logistics manager    |                   1 |
| M0             | Management            | Management - project size      | Office admin         |                   1 |
| M1             | Management            | Management - rate construction | Tool room            |                   1 |
| M1             | Management            | Management - rate construction | Electrician          |                   2 |
| MC0            | Mechanical completion | Mechanical completion          | QC/QA tech           |                   2 |
| ...            | ...                   | ...                            | ...                  |                 ... |

#### `equip_price`

- Equipment name
- Crane capacity tonne
- Equipment price USD per hour
- Cost USD per breakdown
- Fuel consumption gal per day

|   Equipment name |   Crane capacity tonne |   Equipment price USD per hour |   Cost USD per breakdown |   Fuel consumption gal per day |
|------------------|------------------------|--------------------------------|--------------------------|--------------------------------|
| Mobile crane     | 75                     | 35                             |                      nan |                             44 |
| Mobile crane     | 200                    | 149                            |                      nan |                             64 |
| Crawler crane    | 275                    | 217                            |                    37674 |                             76 |
| Crawler crane    | 250                    | 194                            |                    30534 |                             72 |
| Crawler crane    | 400                    | 330                            |                    73375 |                             97 |
| Crawler crane    | 500                    | 420                            |                   101936 |                            113 |
| Crawler crane    | 600                    | 511                            |                   130497 |                            130 |
| Crawler crane    | 750                    | 647                            |                   173339 |                            154 |
| Crawler crane    | 1000                   | 873                            |                   244741 |                            195 |
| Crawler crane    | 1350                   | 1190                           |                   344705 |                            252 |
| ...              | ...                    | ...                            |                      ... |                            ... |

#### `material_price`

- Material type ID
- Material price USD per unit
- Unit

|                   Material type ID |   Material price USD per unit |                          Unit |
|------------------------------------|-------------------------------|-------------------------------|
| unique identifier for the material | price of material per unit    | unit of measure used for cost |
| Concrete 3000 psi                  | 117                           | cubic yard                    |
| Concrete 5000 psi                  | 140                           | cubic yard                    |
| Concrete 8000 psi                  | 130                           | cubic yard                    |
| Steel - rebar                      | 1120                          | ton (short)                   |
| Road base - 3/4 inch crushed stone | 15                            | Loose cubic yard              |
| Excavated dirt                     | 0                             | cubic yard                    |
| Backfill                           | 0                             | cubic yard                    |

#### `rsmeans`

- Operation ID
- Type of cost
- Material type ID
- Rate USD per unit
- Units
- Daily output
- Per Diem Hours (per unit)
- Module
- Number of workers

|                                 Operation ID |     Type of cost |                   Material type ID |   Rate USD per unit | Units                        |   Daily output |   Per Diem Hours (per unit) | Module      |   Number of workers |
|----------------------------------------------|------------------|------------------------------------|---------------------|------------------------------|----------------|-----------------------------|-------------|---------------------|
| Concrete placement                           | Equipment rental | Concrete 5000 psi                  |                4.61 | $/cubic yard                 |                |                             | Foundations |                     |
| Rebar installation                           | Equipment rental | Steel - rebar                      |                0    | $/ton (short)                |                |                             | Foundations |                     |
| Survey                                       | Equipment rental |                                    |                     |                              |                |                             | Roads       |                     |
| Clear and grub                               | Equipment rental |                                    |                     |                              |                |                             | Roads       |                     |
| Topsoil stripping and stockpiling            | Equipment rental |                                    |                1.63 | cubic yard                   |                |                           0 | Roads       |                   1 |
| Stormwater pollution prevention              | Equipment rental |                                    |                     |                              |                |                             | Roads       |                     |
| Culverts                                     | Equipment rental |                                    |                     |                              |                |                             | Roads       |                     |
| Compaction of soil (subgrade and crane path) | Equipment rental |                                    |                1.15 | embankment cubic yards crane |                |                           0 | Roads       |                   3 |
| Mass material movement (cut and fill)        | Equipment rental |                                    |                     |                              |                |                             | Roads       |                     |
| Placing road base (hauling)                  | Equipment rental | Road base - 3/4 inch crushed stone |                5.16 | loose cubic yard             |                |                           0 | Roads       |                   1 |
| ...                                          | ...              | ...                                |                 ... | ...                          |            ,,, |                         ... | ...         |                 ... |

#### `site_facility_building_area`

- Size Min (MW)
- Size Max (MW)
- Building area (sq. ft.)

|   Size Min (MW) |   Size Max (MW) |   Building area (sq. ft.) |
|-----------------|-----------------|---------------------------|
| 0               | 200             | 3000                      |
| 200             | 500             | 5000                      |
| 500             | 800             | 7000                      |
| 800             | 1000            | 9000                      |
| 1000            | 5000            | 12000                     |

#### `weather_window`

The hourly weather profiles uses 4 columns with 3 header rows formatted like the
following table:

|                     | Temperature | Pressure   | Direction | Speed  |
|                     | C           | atm        | Degrees   | m/s    |
|                     | 100         | 100        | 100       | 100    |
| ------------------- | ----------- | ---------- | --------- | ------ |
| 2012-01-01 12:00:00 | 2.444       | 0.95205318 | 185       | 8.681  |
| 2012-01-01 13:00:00 | 1.655       | 0.95227456 | 270       | 7.234  |
| 2012-01-01 14:00:00 | 2.512       | 0.9524854  | 322       | 12.898 |
| 2012-01-01 15:00:00 | 2.589       | 0.953325   | 321       | 14.795 |
| 2012-01-01 16:00:00 | 1.534       | 0.95440628 | 323       | 15.076 |
| 2012-01-01 17:00:00 | 1.014       | 0.95551016 | 322       | 15.53  |
| ...                 | ...         | ...        | ...       | ...    |


## Running LandBOSSE

### Terminal

### `LandBOSSERunner`
