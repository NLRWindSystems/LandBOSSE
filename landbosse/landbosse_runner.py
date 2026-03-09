"""Provides a LandBOSSERunner class to generate results from LandBOSSE without using excel files and
a LandBOSSEResult class to contain these results.
"""

import typing
from copy import deepcopy
from pathlib import Path

import attrs
import pandas as pd

from landbosse.excelio import XlsxReader
from landbosse.excelio.XlsxManagerRunner import XlsxManagerRunner
from landbosse.model import Manager


@attrs.define(auto_attribs=True)
class LandBOSSEResult:
    """Simple class to contain LandBOSSE outputs as DataFrames/Series instead of writing to
    Excel.
    """

    project_parameters: pd.Series = attrs.field(
        validator=attrs.validators.instance_of(pd.Series),
    )
    data_sheets: dict = attrs.field(converter=dict)
    model_variables: pd.DataFrame = attrs.field(
        validator=attrs.validators.instance_of(pd.DataFrame),
    )
    operation_cost: pd.DataFrame = attrs.field(
        validator=attrs.validators.instance_of(pd.DataFrame),
    )


@attrs.define(auto_attribs=True)
class LandBOSSERunner:
    """Allows calling of LandBOSSE without using Excel files as outputs."""

    expected_config: typing.ClassVar[dict] = {
        "id": "Name of the project",
        "enable_cost_and_scaling_modifications": "Should cost and scaling modifications be applied "
        "(true/false)",
        "construction_months": "Total construction duration (months)",
        "turbine_rating_MW": "Capacity of turbine (MW)",
        "hub_height_m": "Turbine hub height (m)",
        "rotor_diameter_m": "Turbine rotor diameter (m)",
        "turbine_spacing_rotor_diameter": "Layout spacing between turbines in each row, in rotor "
        "diameters",
        "row_spacing_rotor_diameter": "Layout spacing between rows, in rotor diameters",
        "num_turbines": "Number of turbines",
        "turbine_capex": "CapEx of turbine ($/kW)",
        "base_topping_breakpoint": "Height at which cranes change from 'Base' to 'Topping', "
        "represented as a fraction of hub height",
        "fuel_cost_usd_per_gal": "Cost of fuel per gallon ($/gal)",
        "turbine_delivery_rate_per_week": "Number of turbine deliveries (all components) per week",
        "wind_shear": "Wind shear (assumed constant across all timestamps and turbines)",
        "foundation_depth_m": "Depth of concrete foundation (m)",
        "rated_thrust_N": "Rated horizontal thrust of turbine (N)",
        "bearing_pressure_Pa": "Bearing pressure capacity of soil underneath foundations (Pa)",
        "gust_velocity_50_year_m/s": "50 year wind gust velocity (m/s)",
        "line_frequency": "Electrical frequency of grid (Hz)",
        "combined_homerun_trench_length_km": "Combined homerun trench length to substation (km) "
        "(optional - can be null but cannot be omitted)",
        "non_erection_wind_delay_critical_height_m": "When calculating wind delays for non-erection"
        " tasks, shear values to this height (m)",
        "non_erection_wind_delay_critical_wind_speed_m/s": "When calculating wind delays for "
        "non-erection tasks, wind speeds above this value will force work to stop (m/s)",
        "distance_to_interconnect_mi": "Distance from substation to switchyard (miles)",
        "interconnect_voltage_kV": "Voltage of grid (kV)",
        "new_switchyard": "Should a new switchyard be built (true/false)",
        "road_length_adder_m": "Distance from site entry point to the project (m)",
        "road_quality": "Non-dimensional representation of the quality of roads. 0 is poor quality,"
        " 1 is good quality. A higher road quality reduces the total road cost",
        "percent_roads_to_be_constructed": "What percentage of roads need to be constructed vs "
        "already exist",
        "road_width_ft": "Width of roads (ft)",
        "road_thickness_in": "Thickness of roads (in)",
        "calculate_road_cost_for_distributed_wind": "Should road costs be included in the "
        "calculation for distributed wind projects (true/false)",
        "site_prep_area_for_distributed_wind_m2": "Site prep area for distributed wind projects "
        "(m^2)",
        "crane_width_m": "Width of crane (m)",
        "num_highway_permits": "Number of highway permits required",
        "num_access_roads": "Number of site access roads required",
        "overtime_multiplier": "Labor cost multiplier for overtime work",
        "allow_same_flag": "flag to indicate whether choosing same base and topping crane is "
        "allowed (true/false)",
        "override_total_management_cost_for_distributed": "For distributed wind project, override "
        "the calculated management cost and use this value instead (0 means do not override)",
        "markup_contingency": "Markup contingency",
        "markup_warranty_management": "Markup warranty management",
        "markup_sales_and_use_tax": "Markup sales and use tax",
        "markup_overhead": "Markup overhead",
        "markup_profit_margin": "Markup profit margin",
        "utility_interconnection_fees_distributed_wind": "Fee for connecting to the grid "
        "(distributed wind projects only)",
        "labor_cost_multiplier": "Multiplier to modify labor costs",
        "crane_breakdown_fraction": "What fraction of cranes will breakdown. 0 means none, 1 means "
        "all. Breakdowns increase the total erection duration",
        "user_trench_length_flag": "Flag (0 = no; 1 = yes) to indicate if the user-defined trench length should be used"
    }

    # Mapping from new parameter input names to those expected by LandBOSSE
    keys_rename: typing.ClassVar[dict] = {
        "id": "Project ID",
        "data_tables": "Project data file",
        "construction_months": "Total project construction time (months)",
        "turbine_rating_MW": "Turbine rating MW",
        "hub_height_m": "Hub height m",
        "rotor_diameter_m": "Rotor diameter m",
        "turbine_spacing_rotor_diameter": "Turbine spacing (times rotor diameter)",
        "row_spacing_rotor_diameter": "Row spacing (times rotor diameter)",
        "num_turbines": "Number of turbines",
        "turbine_capex": "Turbine Capex (USD/kW)",
        "base_topping_breakpoint": "Breakpoint between base and topping (percent)",
        "fuel_cost_usd_per_gal": "Fuel cost USD per gal",
        "turbine_delivery_rate_per_week": "Rate of deliveries (turbines per week)",
        "wind_shear": "Wind shear exponent",
        "foundation_depth_m": "Foundation depth m",
        "rated_thrust_N": "Rated Thrust (N)",
        "bearing_pressure_Pa": "Bearing Pressure (n/m2)",
        "gust_velocity_50_year_m/s": "50-year Gust Velocity (m/s)",
        "line_frequency": "Line Frequency (Hz)",
        "combined_homerun_trench_length_km": "Combined homerun trench length to substation " "(km)",
        "non_erection_wind_delay_critical_height_m": "Non-Erection Wind Delay Critical Height "
        "(m)",
        "non_erection_wind_delay_critical_wind_speed_m/s": "Non-Erection Wind Delay Critical "
        "Speed (m/s)",
        "distance_to_interconnect_mi": "Distance to interconnect (miles)",
        "interconnect_voltage_kV": "Interconnect Voltage (kV)",
        "new_switchyard": "New Switchyard (y/n)",
        "road_length_adder_m": "Road length adder (m)",
        "road_quality": "Road Quality (0-1)",
        "percent_roads_to_be_constructed": "Percent of roads that will be constructed",
        "road_width_ft": "Road width (ft)",
        "road_thickness_in": "Road thickness (in)",
        "calculate_road_cost_for_distributed_wind": "Calculate road cost for distributed wind? "
        "(y/n)",
        "site_prep_area_for_distributed_wind_m2": "Site prep area for Distributed wind (m2)",
        "crane_width_m": "Crane width (m)",
        "num_highway_permits": "Number of highway permits",
        "num_access_roads": "Number of access roads",
        "overtime_multiplier": "Overtime multiplier",
        "allow_same_flag": "Allow same flag",
        "override_total_management_cost_for_distributed": "Override total management cost for "
        "distributed (0 does not override)",
        "markup_contingency": "Markup contingency",
        "markup_warranty_management": "Markup warranty management",
        "markup_sales_and_use_tax": "Markup sales and use tax",
        "markup_overhead": "Markup overhead",
        "markup_profit_margin": "Markup profit margin",
        "utility_interconnection_fees_distributed_wind": "Utility Interconnection Fees (Small "
        "DW only)",
        "labor_cost_multiplier": "Labor cost multiplier",
        "crane_breakdown_fraction": "Crane breakdown fraction",
        "combined_homerun_trench_length_km": "Combined Homerun Trench Length to Substation (km)", 
        "user_trench_length_flag": "Flag for user-defined home run trench length (0 = no; 1 = yes)",
    }

    input_config: dict = attrs.field(converter=dict)
    weather: pd.DataFrame = attrs.field(
        default=None,
        validator=attrs.validators.optional(attrs.validators.instance_of(pd.DataFrame)),
    )
    result: LandBOSSEResult = attrs.field(
        validator=attrs.validators.instance_of(LandBOSSEResult),
        init=False,
    )

    def __attrs_post_init__(self):
        self.check_expected_configs_are_provided(self.input_config)

    @staticmethod
    def convert_excel_to_dict(
        filename: str | Path,
        project_id: str,
        *,
        enable_cost_and_scaling_modifications: bool = False,
    ) -> dict:
        """Convert a :py:attr:`project_id` from an Excel project list to a ``LandBOSSERunner``
        compliant dictionary.

        Parameters
        ----------
        filename : str | Path
            The project list file where the project's data can be found.
        project_id : str
            The ID for the project in the "Project ID" column of the project list.
        enable_cost_and_scaling_modifications : bool, optional
            Whether or not to enable the cost and scaling modifications, by default False.

        Returns
        -------
        dict
            The project listing data for a given :py:attr:`project_id` converted to a ``LandBOSSERunner``-compliant
            format.
        """
        df = pd.read_excel(filename)
        data = df.loc[df["Project ID"].eq(project_id)].reset_index(drop=True).loc[0].to_dict()
        keys_rename = {v: k for k, v in LandBOSSERunner.keys_rename.items()}
        data = {keys_rename.get(k, k): v for k, v in data.items()}
        data["enable_cost_and_scaling_modifications"] = enable_cost_and_scaling_modifications
        return data

    def check_expected_configs_are_provided(self, input_config: dict) -> None:
        """Checks to ensure all inputs required by the model have been provided.

        Args:
            input_config (dict): input configuration dict
        """

        # Check for any missing inputs
        missing_parameters = set(self.expected_config.keys()).difference(
            input_config.keys()
        )
        if bool(missing_parameters):
            msg_lines = "\n\t".join(
                f"{mp:s}: {str(self.expected_config[mp]):s}" for mp in missing_parameters
            )
            msg = f"The following LandBOSSE parameters are missing:\n{msg_lines:s}"
            raise ValueError(msg)

    def get_project_parameters(self) -> pd.Series:
        """Read inputs from the YAML file and convert into a format expected by LandBOSSE.

        Raises
        ------
        ValueError
            Raised if any parameters are missing.

        Returns
        -------
        pd.Series
            Series containing input parameters for LandBOSSE with the required names
        dict[str, pd.DataFrame]
            Dictionary of the Excel project data with each sheet's name as a key and the
            data loaded as a pandas DataFrame.
        """
        project_parameters_dict = deepcopy(self.input_config)
        data_sheets = project_parameters_dict.pop("data_tables")

        # Convert parameters dict to pandas Series (LandBOSSE expects a Series)
        project_parameters = pd.Series(project_parameters_dict, name="value")
        project_parameters = project_parameters.rename_axis("parameter")
        project_parameters = project_parameters.rename(self.keys_rename)

        # Convert some bool inputs to int or string based on LandBOSSE requirements
        if "Combined Homerun Trench Length to Substation (km)" in project_parameters.index:
            project_parameters["Flag for user-defined home run trench length (0 = no; 1 = yes)"] = 1
        else:
            project_parameters["Flag for user-defined home run trench length (0 = no; 1 = yes)"] = 0
            project_parameters["Combined Homerun Trench Length to Substation (km)"] = None

        project_parameters["New Switchyard (y/n)"] = (
            "y" if project_parameters["New Switchyard (y/n)"] else "n"
        )

        project_parameters["Project ID with serial"] = project_parameters["Project ID"]

        return project_parameters, data_sheets

    def run(self) -> None:
        """Run the LandBOSSE model and save outputs in a LandBOSSEResult object instead of excel
        spreadsheets.

        Returns
        -------
        LandBOSSEResult
            Outputs from LandBOSSE model
        """
        project_parameters, data_sheets = self.get_project_parameters()

        # Prioritize weather profile provided at initialization over existing "weather_window" in Excel
        if self.weather is not None:
            data_sheets["weather_window"] = self.add_header_to_weather_dataframe(self.weather)

        xlsx_reader = XlsxReader()
        xlsx_reader.modify_project_data_and_project_list(data_sheets, project_parameters)

        # Apply cost and scaling modifications if needed.
        enable_cost_and_scaling_modifications = project_parameters[
            "enable_cost_and_scaling_modifications"
            ]
        if enable_cost_and_scaling_modifications:
            xlsx_reader.apply_cost_and_scaling_modifications_to_project_parameters(
                project_parameters
            )

        master_input_dict = xlsx_reader.create_master_input_dictionary(
            data_sheets,
            project_parameters,
        )

        output_dict: dict = {}
        mc = Manager(input_dict=master_input_dict, output_dict=output_dict)
        mc.execute_landbosse(project_name=project_parameters["Project ID with serial"])

        # Extract result dataframes
        runs_dict = {project_parameters["Project ID with serial"]: output_dict}
        model_variables = pd.DataFrame(XlsxManagerRunner.extract_details_lists(None, runs_dict))
        operation_cost = pd.DataFrame(
            XlsxManagerRunner.extract_module_type_operation_lists(None, runs_dict),
        )

        # Save outputs into LandBOSSEResult object
        self.result = LandBOSSEResult(
            project_parameters=project_parameters,
            data_sheets=data_sheets,
            model_variables=model_variables,
            operation_cost=operation_cost,
        )

    @staticmethod
    def add_header_to_weather_dataframe(weather_window: pd.DataFrame) -> pd.DataFrame:
        """Add blank header rows to a weather dataframe to match the format expected by
         LandBOSSE.

        Returns
        -------
        pd.DataFrame
            Weather dataframe with blank header.
        """
        NUM_HEADER_ROWS = 5
        WEATHER_COLUMNS = [
            "datetime",
            "surface_temperature",
            "surface_pressure",
            "wind_direction",
            "windspeed",
            ]

        weather_window = weather_window.reset_index()

        # Check required weather columns are present
        missing_columns = set(WEATHER_COLUMNS).difference(weather_window.columns)
        if bool(missing_columns):
            missing_columns_msg = (
                "The following columns are required but missing from the weather data: "
                f"{', '.join(sorted(missing_columns))}"
            )
            raise ValueError(missing_columns_msg)

        # select columns required by LandBOSSE
        weather_window = weather_window[WEATHER_COLUMNS]

        # Combine the weather data with blank header rows
        weather_window = pd.concat(
            objs=(
                pd.DataFrame(index=range(NUM_HEADER_ROWS), columns=weather_window.columns).astype(
                    weather_window.dtypes
                ),
                weather_window,
            ),
            ignore_index=True,
        )
        return weather_window


if __name__ == "__main__":
    pass
