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

Component
: Name of the component; can be specific or generic. For items where there are more than one of them
  or they are are part of a whole like tower sections or blades, number them using 1-indexing,
  e.g., "Tower 1", "Tower 2", "Tower 3".

Mass tonne
: Mass in metric tonnes.

Lift height m
: Height, in $m$, that a crane will have to lift the component in order to complete assembly.

Surface area sq m
: Total surface area, in $m^2$, of a cross-section of the component. This will be used for
  calculating thefoundational load.

Coeff drag
: Coefficient of drag. This will be used to understand the effective mass while lifting the component.

Coeff drag (installed)
: Coefficient of drag once the component is installed. This will be used for calculating the
  foundational load.

Section height m
: Total height ($m$) of a cross-section of the component. This will be used for calculating the
  foundational load.

Lever arm m
: Perpendicular distance, in $m$, from center of the foundation.

Cycle time installation hrs
: Amount of time, in hours, required to prepare the component for assembly.

Offload hook height m
: Height of the hook ($m$) above the top of the component to account for the total height of the crane's lift.

Offload cycle time hrs
: Amount of time (in hours) required to detach the component from the crane.

Multplier drag rotor
: Multiplier for accounting for the additional drag of the rotor for computing the foundation load.
  This should only apply to the nacelle and blades

Multiplier tower drag
: Multiplier for accounting for the additional drag of the tower for computing the foundation load.

The following data are used for the GE 1.5 MW public example (`ge15_public.xlsx`).

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

Array Cable
: Name or type of the array cable.

Conductor Size (mm2)
: Cable cross section, in $mm^2$.

Current Capacity (A)
: Cable current capacity at 1m burial depth, in $A$.

Rated Voltage (V)
: Cable rated line-to-line voltage, in $V$.

AC Resistance (Ohms/km)
: Cable resistance for the AC current per kilometer, in $\frac{\omega}{km}$

Inductance (mH/km)
: Cable inductance per kilometer, in $\frac{mH}{km}$

Capacitance (nF/km)
: Cable capacitance per kilometer, in $\frac{nF}{km}$

Cost (USD/LF)
: Cost of the cable per linear foot ($\frac{USD}{LF}$).

The following data are used for the GE 1.5 MW public example (`ge15_public.xlsx`).

| Array Cable   |   Conductor Size (mm2) |   Current Capacity (A) |   Rated Voltage (V) |   AC Resistance (Ohms/km) |   Inductance (mH/km) |   Capacitance (nF/km) |   Cost (USD/LF) |
|---------------|------------------------|------------------------|---------------------|---------------------------|----------------------|-----------------------|-----------------|
| AWG 1/0       |                    120 |                    300 |                  36 |                    0.253  |                0.398 |                 0.179 |               6 |
| AWG 4/0       |                    240 |                    440 |                  36 |                    0.125  |                0.359 |                 0.223 |               9 |
| MCM 500       |                    500 |                    640 |                  36 |                    0.0605 |                0.317 |                 0.293 |              13 |
| MCM1000       |                    800 |                    830 |                  36 |                    0.0367 |                0.291 |                 0.375 |              16 |
| MCM1250       |                   1000 |                    935 |                  36 |                    0.0291 |                0.284 |                 0.411 |              17 |

#### `equip`

Equipment ID
: Unique identififer for the equipment group.

Operation
: One of "Top", "Base", or "Offload" to indicate what grouping of operations the equipment can
  perform.

Equipment name
: Name of the equipment in the equipment group.

Crane capacity tonne
: Maximum capacityof the crane, in metric tonnes.

Number of equipment
: Number of the equipment used during the operation.

The following subset of the data are used for the GE 1.5 MW public example (`ge15_public.xlsx`).

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

Equipment name
: Name matching with the `equip` sheet.

Crane name
: Crane model name

Boom system
: Type of boom system used on the crane. Primarily used for logging crane details.

Crane capacity tonne
: Maximum crane capacity. Used for matching cranes to components for ideal assembly costs and speeds.

Speed of travel km per hr
: Ground travel speed, in $km/h$

Hoist speed m per min
: Crane lifting rate, in $m/min$.

Crew type ID
: Unique identifer for the type of crew required for the operation.

Equipment ID
: Unique identifier matching with the `equip` sheet.

Setup time hr
: Amount of time, in hours, required for the crane to be prepared at a new lift location.

Breakdown time hr
: Amount of time, in hours, required for the crane to be broken down prior to being moved to a new
  lift location.

Max wind speed m per s
: Maximum allowable windspeed allowed during operations, in $m/s$.

Hub height m
: Maximum lift height for the crane, in $m$.

Max capacity tonne
: Maximum lift capacity for the crane, in metric tonnes.

Radius m
: Undefined, and potentially unused.

Hook Height m
: Height of the hook above the top of the component to be lifted. Used for the total lift mass and
  wind speed calculations.

Mobilization cost USD
: Cost to mobilize the crane for the duration of the installation period, in USD.

The following subset of the data are used for the GE 1.5 MW public example (`ge15_public.xlsx`).

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

Type of cost
: Development cost category.

Cost USD
: Total cost, in USD.

Phase of construction
: Phase of construction where the cost is incurred, likely alway "Development".

The following data are used for the GE 1.5 MW public example (`ge15_public.xlsx`).

|     Type of cost |   Cost USD |   Phase of construction |
|------------------|------------|-------------------------|
| Equipment rental | 0          | Development             |
| Labor            | 1000000    | Development             |
| Materials        | 0          | Development             |
| Mobilization     | 0          | Development             |
| Other            | 0          | Development             |

#### `crew_price`

Labor type ID
: Unique labor type identifier, matching with `crew`.

Hourly rate USD per hour
: Hourly cost of the crew per hour, in $USD/hr$.

Per diem USD per day
: Daily cost for food, etc. for the type of crew member, in $USD/day$.

The following subset of the data are used for the GE 1.5 MW public example (`ge15_public.xlsx`).

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

Crew type ID
: Unique crew type identifier, matching with `crane_specs`

Operation
: General operational category for the type of crew member.

Crew name
: Name of the crew type.

Labor type ID
: Unique labor type identifier for the type of crew member.

Number of workers
: Number of workers in the labor type that make up one unit of the crew.

The following subset of the data are used for the GE 1.5 MW public example (`ge15_public.xlsx`).

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

Equipment name
: Name of the equipment.

Crane capacity tonne
: Maximum capacity of the crane, in metric tonnes.

Equipment price USD per hour
: Hourly cost of the equipment, in $USD/hr$.

Cost USD per breakdown
: Total cost to breakdown the equipment before moving to another lift site, in USD.

Fuel consumption gal per day
: Expected daily fuel consumption, in $gal/day$.

The following subset of the data are used for the GE 1.5 MW public example (`ge15_public.xlsx`).

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

Material type ID
: Unique material identifier

Material price USD per unit
: Cost of the materials per unit, in $USD/unit$.

Unit
: Measurement units used for measuring the material's quantity.

The following data are used for the GE 1.5 MW public example (`ge15_public.xlsx`).

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

Operation ID
: Unique identifier for the operation.

Type of cost
: Cost category.

Material type ID
: Type of material used, should match `material_price`.

Rate USD per unit
: Cost per unit, in $USD/unit$

Units
: Measurment units.

Daily output
: Daily output of the operation.

Per Diem Hours (per unit)
: Additional hourly per diem costs per measured unit.

Module
: Construction phase category. Should be one of "Foundations", "Roads", or "Collection".

Number of workers
: Number of workers required for the operation type.

The following subset of data are used for the GE 1.5 MW public example (`ge15_public.xlsx`).

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
| ...                                          | ...              | ...                                |                 ... | ...                          |            ... |                         ... | ...         |                 ... |

#### `site_facility_building_area`

Size Min (MW)
: Minimum wind power plant size to estimate the site facility building size, in $MW$.

Size Max (MW)
: Maximum wind power plant size to estimate the site facility building size, in $MW$.

Building area (sq. ft.)
: Building size for site facilities, in ${ft}^2$.

The following data are used for the GE 1.5 MW public example (`ge15_public.xlsx`).

|   Size Min (MW) |   Size Max (MW) |   Building area (sq. ft.) |
|-----------------|-----------------|---------------------------|
| 0               | 200             | 3000                      |
| 200             | 500             | 5000                      |
| 500             | 800             | 7000                      |
| 800             | 1000            | 9000                      |
| 1000            | 5000            | 12000                     |

#### `weather_window`

The hourly weather profiles uses 4 columns with 3 header rows formatted like the following table.
In the following data, taken from the GE 1.5 MW public example (`ge15_public.xlsx`), the first
row should contain the measurement units, and the second row should indicate the height at which
the measurement was taken, in $m$.

|                     | Temperature | Pressure   | Direction | Speed  |
| ------------------- | ----------- | ---------- | --------- | ------ |
|                     | C           | atm        | Degrees   | m/s    |
|                     | 100         | 100        | 100       | 100    |
| 2012-01-01 12:00:00 | 2.444       | 0.95205318 | 185       | 8.681  |
| 2012-01-01 13:00:00 | 1.655       | 0.95227456 | 270       | 7.234  |
| 2012-01-01 14:00:00 | 2.512       | 0.9524854  | 322       | 12.898 |
| 2012-01-01 15:00:00 | 2.589       | 0.953325   | 321       | 14.795 |
| 2012-01-01 16:00:00 | 1.534       | 0.95440628 | 323       | 15.076 |
| 2012-01-01 17:00:00 | 1.014       | 0.95551016 | 322       | 15.53  |
| ...                 | ...         | ...        | ...       | ...    |

## Running LandBOSSE

The two primary means for running LandBOSSE are through the terminal using only Excel-based data,
or through Python (script, IDE, Jupyter Notebook, etc.). The following sections will walk through
running LandBOSSE through each of these methods.

### Terminal

Per the installation instructions, this example assumes your conda (or other) Python environment
has been created and LandBOSSE has been installed.

1. Determine the desired input and output folder locations for your data.
2. Configure your project listing Excel file and the project data Excel file for each listed project
   described in [Project Input Data](#project-input-data).
   
   :::{important} The name of the project listing must be called `project_list.xlsx` as it will
   be the only file that is used for running projects.
   :::

3. Open a terminal (or Anaconda Prompt or other) session.
4. Navigate to where LandBOSSE has been downloaded. In the terminal:
   
   ```bash
   cd /path/to/LandBOSSE
   ```

5. Activate your Python environment. For conda environments, but be sure to use the name of your
   environment:

    ```bash
    conda activate landbose
    ```

6. Run all validLandBOSSE, where `-i` can be substituted for `--input`, and `-o` for `--output`.

    ```bash
    python main.py -i /path/to/input-folder -o /path/to/output-folder
    ```

    Additional run flags also exist:

    - `-s` or `--scaling` for scaling study mode. This method modifies each row of the project list
      after it has been modified by the parameters for to scale certain input values based on what
      has been parametrically modified.
    - `-v` or `--validate` which creates the file path for the output file from prior LandBOSSE run
      that will be used to check latest run. The validation output file must be in the inputs folder
      and must be called `landbosse-output-validation.xlsx`.

### `LandBOSSERunner`

1. Determine the desired input and output folder locations for your data.
2. Configure your project listing Excel file and the project data Excel file for each listed project
   described in [Project Input Data](#project-input-data).
3. In a Python script, Jupyter Notebook, etc., some form of the following code can be used to run
   a single project listing.

   ```python
   from pathlib import Path
   
   import yaml
   import pandas as pd
 
   from landbosse.landbosse_runner import LandBOSSERunner

   # If your data are stored in a YAML file (preferable), load them first, or
   # create a data dictionary in place of the following code.
   with Path("/path/to/my_project_data.yaml").open() as f:
       inputs = yaml.safe_load(f)

   # Load the Excel project data. If the value of "data_tables" is relative to where the
   # code will be run, simply exclude the `data_path` portion of the following code.
   data_path = Path("/path/to/data_tables/").resolve()
   inputs["data_tables"] = pd.read_excel(
       data_path /inputs["data_tables"], sheet_name=None
   )

   # Optional: load alternative weather data
   weather = pd.read_csv("/my/weather/data.csv")  # replace csv with your file format
   weather = LandBOSSERunner.add_header_to_weather_dataframe(weather)

   # Create your runner object, and run the analysis. Simply exclude the weather
   # keyword argument if yours is contained in the `data_tables`
   lb = LandBOSSERunner(input_config=inputs, weather=weather)
   lb.run()
   ```

4. Once the above code (or similar) is successfully run, the `result` object is created and attched
   to the `LandBOSSERunner`. For complete details please see the `LandBOSSEResult` API documentation.
   The `lb.result` (using the above examples naming convention for the runner object) contains the
   following attributes as separate Pandas Series or DataFrames, and can be saved to CSV or one
   Excel book as desired.

   - `project_parameters`: The values provided from the input dictionary.
   - `data_sheets`: The Excel project data loaded as a dictionary of dataframes.
   - `model_variables`: A copy of the model details that would traditionally be saved to Excel
     when running LandBOSSE through the terminal.
   - `operation_cost`: The detailed operational cost logs for the simulated installation.
