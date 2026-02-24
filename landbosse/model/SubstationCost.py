import traceback
import pandas as pd
import math

from .CostModule import CostModule


class SubstationCost(CostModule):
    """
    Calculates the costs associated with substations for land-based wind projects *(module is currently based on curve fit of empirical data)*

    Calculation consists of the following steps:
    
    * Get project size: ``project_size_megawatts = num_turbines * turbine_rating_kilowatt / kilowatt_per_megawatt``
    * Get interconnect voltage

    Keys in the input dictionary are the following:

    interconnect_voltage_kV : int
        project interconnection voltage to substation [in kV
    project_size_megawatts : int
        total project size [in MW]

    Keys in the output dictionary are the following:

    substation_cost : float
        cost of substation [in USD]

    Created by Annika Eberle and Owen Roberts on Dec. 17, 2018 and refactored by Parangat Bhaskar and Alicia Key on  June 3, 2019

    """
    def __init__(self, input_dict, output_dict, project_name):
        """
        Parameters
        ----------
        input_dict : dict
            The input dictionary with key value pairs described in the
            class documentation

        output_dict : dict
            The output dictionary with key value pairs as found on the
            output documentation.
        """
        self.input_dict = input_dict
        self.output_dict = output_dict
        self.project_name = project_name


    def calculate_costs(self, calculate_costs_input_dict , calculate_costs_output_dict):
        """
        Calculates the total substation cost in USD

        Parameters
        ----------
        Uses the following from ``calculate_costs_input_dict``

            interconnect_voltage_kV : float
                Interconnection voltage, in kV.
            project_size_megawatts : float
                Project capacity, in MW.

        Returns
        -------
        substation_cost : float
            Total substation cost, in USD.
        """

        # Run in utility mode if number of turbines is > 10:
        if calculate_costs_input_dict['num_turbines'] > 10:
            calculate_costs_output_dict['substation_cost_usd'] = 11652 * (
                        calculate_costs_input_dict['interconnect_voltage_kV'] + calculate_costs_input_dict[
                    'project_size_megawatts']) + 11795 * (calculate_costs_input_dict[
                                                              'project_size_megawatts'] ** 0.3549) + 1526800
        # Run in distributed mode if number of turbines is <= 10:
        else:
            calculate_costs_output_dict['substation_cost_usd'] = 0

        calculate_costs_output_dict['substation_cost_output_df'] = pd.DataFrame([['Other', calculate_costs_output_dict['substation_cost_usd'], 'Substation']],
                                                 columns=['Type of cost', 'Cost USD', 'Phase of construction'])

        calculate_costs_output_dict['total_substation_cost'] = calculate_costs_output_dict['substation_cost_output_df']

        return calculate_costs_output_dict['substation_cost_output_df']

    def outputs_for_detailed_tab(self, input_dict, output_dict):
        """
        Creates a list of dictionaries which can be used on their own or
        used to make a dataframe.

        Must be called after :py:meth:`run_module`.

        Returns
        -------
        list[dict]
            A list of dicts, with each dict representing a row of the data.
        """
        result = []
        module = type(self).__name__

        for row in self.output_dict['substation_cost_output_df'].itertuples():
            dashed_row = '{} <--> {} <--> {}'.format(row[1], row[3], math.ceil(row[2]))
            result.append({
                'unit': '',
                'type': 'dataframe',
                'variable_df_key_col_name': 'Type of Cost <--> Phase of Construction <--> Cost in USD ',
                'value': dashed_row,
                'last_number': row[2]
            })

        for _dict in result:
            _dict['project_id_with_serial'] = self.project_name
            _dict['module'] = module

        self.output_dict['substation_cost_csv'] = result
        return result


    def run_module(self):
        """
        Runs the SubstationCost module and populates the IO dictionaries with calculated values.

        Returns
        -------
        tuple
            First element of tuple contains a 0 or 1. 0 means no errors happened and
            1 means an error happened and the module failed to run. The second element
            either returns a 0 if the module ran successfully, or it returns the error
            raised that caused the failure.

        """
        try:
            self.calculate_costs(self.input_dict, self.output_dict)
            self.outputs_for_detailed_tab(self.input_dict, self.output_dict)
            # self.outputs_for_module_type_operation(self.input_dict, self.output_dict)
            self.output_dict['substation_module_type_operation'] = self.outputs_for_costs_by_module_type_operation(
                input_df=self.output_dict['substation_cost_output_df'],
                project_id=self.project_name,
                total_or_turbine=True
            )
            return 0, 0
        except Exception as error:
            traceback.print_exc()
            print(f"Fail {self.project_name} SubstationCost")
            return 1, error
