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


==================================================================== =============================================== ===============================================================================================================================================
Project List Column                                                  LandBOSSE Runner Key                            Description
==================================================================== =============================================== ===============================================================================================================================================
Project ID                                                           id                                              Name of the project
Project data file                                                    datafile                                        ERROR
Total project construction time (months)                             construction_months                             Total construction duration (months)
Turbine rating MW                                                    turbine_rating_MW                               Capacity of turbine (MW)
Hub height m                                                         hub_height_m                                    Turbine hub height (m)
Rotor diameter m                                                     rotor_diameter_m                                Turbine rotor diameter (m)
Turbine spacing (times rotor diameter)                               turbine_spacing_rotor_diameter                  Layout spacing between turbines in each row, in rotor diameters
Row spacing (times rotor diameter)                                   row_spacing_rotor_diameter                      Layout spacing between rows, in rotor diameters
Number of turbines                                                   num_turbines                                    Number of turbines
Turbine Capex (USD/kW)                                               turbine_capex                                   CapEx of turbine ($/kW)
Breakpoint between base and topping (percent)                        base_topping_breakpoint                         Height at which cranes change from 'Base' to 'Topping', represented as a fraction of hub height
Fuel cost USD per gal                                                fuel_cost_usd_per_gal                           Cost of fuel per gallon ($/gal)
Rate of deliveries (turbines per week)                               turbine_delivery_rate_per_week                  Number of turbine deliveries (all components) per week
Wind shear exponent                                                  wind_shear                                      Wind shear (assumed constant across all timestamps and turbines)
Foundation depth m                                                   foundation_depth_m                              Depth of concrete foundation (m)
Rated Thrust (N)                                                     rated_thrust_N                                  Rated horizontal thrust of turbine (N)
Bearing Pressure (n/m2)                                              bearing_pressure_Pa                             Bearing pressure capacity of soil underneath foundations (Pa)
50-year Gust Velocity (m/s)                                          gust_velocity_50_year_m/s                       50 year wind gust velocity (m/s)
Line Frequency (Hz)                                                  line_frequency                                  Electrical frequency of grid (Hz)
Combined homerun trench length to substation (km)                    combined_homerun_trench_length_km               Combined homerun trench length to substation (km) (optional - can be null but cannot be omitted)
Non-Erection Wind Delay Critical Height (m)                          non_erection_wind_delay_critical_height_m       When calculating wind delays for non-erection tasks, shear values to this height (m)
Non-Erection Wind Delay Critical Speed (m/s)                         non_erection_wind_delay_critical_wind_speed_m/s When calculating wind delays for non-erection tasks, wind speeds above this value will force work to stop (m/s)
Distance to interconnect (miles)                                     distance_to_interconnect_mi                     Distance from substation to switchyard (miles)
Interconnect Voltage (kV)                                            interconnect_voltage_kV                         Voltage of grid (kV)
New Switchyard (y/n)                                                 new_switchyard                                  Should a new switchyard be built (true/false)
Road length adder (m)                                                road_length_adder_m                             Distance from site entry point to the project (m)
Road Quality (0-1)                                                   road_quality                                    Non-dimensional representation of the quality of roads. 0 is poor quality, 1 is good quality. A higher road quality reduces the total road cost
Percent of roads that will be constructed                            percent_roads_to_be_constructed                 What percentage of roads need to be constructed vs already exist
Road width (ft)                                                      road_width_ft                                   Width of roads (ft)
Road thickness (in)                                                  road_thickness_in                               Thickness of roads (in)
Calculate road cost for distributed wind? (y/n)                      calculate_road_cost_for_distributed_wind        Should road costs be included in the calculation for distributed wind projects (true/false)
Site prep area for Distributed wind (m2)                             site_prep_area_for_distributed_wind_m2          Site prep area for distributed wind projects (m^2)
Crane width (m)                                                      crane_width_m                                   Width of crane (m)
Number of highway permits                                            num_highway_permits                             Number of highway permits required
Number of access roads                                               num_access_roads                                Number of site access roads required
Overtime multiplier                                                  overtime_multiplier                             Labor cost multiplier for overtime work
Allow same flag                                                      allow_same_flag                                 flag to indicate whether choosing same base and topping crane is allowed (true/false)
Override total management cost for distributed (0 does not override) override_total_management_cost_for_distributed  For distributed wind project, override the calculated management cost and use this value instead (0 means do not override)
Markup contingency                                                   markup_contingency                              Markup contingency
Markup warranty management                                           markup_warranty_management                      Markup warranty management
Markup sales and use tax                                             markup_sales_and_use_tax                        Markup sales and use tax
Markup overhead                                                      markup_overhead                                 Markup overhead
Markup profit margin                                                 markup_profit_margin                            Markup profit margin
Utility Interconnection Fees (Small DW only)                         utility_interconnection_fees_distributed_wind   Fee for connecting to the grid (distributed wind projects only)
Labor cost multiplier                                                labor_cost_multiplier                           Multiplier to modify labor costs
Crane breakdown fraction                                             crane_breakdown_fraction                        What fraction of cranes will breakdown. 0 means none, 1 means all. Breakdowns increase the total erection duration
==================================================================== =============================================== ===============================================================================================================================================


### Project Excel Data

## Running LandBOSSE

### Terminal

### `LandBOSSERunner`
