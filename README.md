# MSSP_Model_Library_Type2_Endogenous
## A Library of Multi-Stage Stochastic Programming Models with Type 2 Endogenous Uncertainty (Shoji & Cremaschi, 2026)
## Summary
This repository contains the code for 13 MSSP models along with the instance data to replicate the results from 
  >Shoji, Y. & Cremaschi, S. (2026). <br />
  >A Library of Multi-Stage Stochastic Programming Models with Type 2 Endogenous Uncertainty. <br />
  >Computers & Chemical Engineering 

The nomenclatures and formulations for these models are provided in the Supplementary Material of the paper. <br />
In addition, this repository includes an analysis tool for scenario tree information, ScenarioTreeAnalizer. See the ScenarioTreeAnalizer section for further details.

## Quickstart
1. Clone the repository to obtain a copy of the source code.

2. Open the `main.py` file.

3. Select the model name.
    ```
    problem_name = 'model_name_abbreviation' 
    ```
    The abbreviations for the 13 models are: <br />
    
    - Size – Size problem (Jonsbråten et al., 1998; Goel & Grossmann, 2006b) <br />
    - OGFDP – Offshore Gas Field Development Planning problem (Goel & Grossmann, 2004; Goel & Grossmann, 2006a) <br />
    - CTP – Clinical Trial Planning problem (Colvin & Maravelias, 2008) <br />
    - OPMPSP – Open Pit Mine Production Scheduling Problem (Boland et al., 2008) <br />
    - PNS – Process Network Synthesis problem (Tarhan & Grossmann, 2008) <br />
    - RD – R&D Project Portfolio Management problem (Solak et al., 2010) <br />
    - OOFIP – Offshore OilField Infrastructure Planning problem (Gupta and Grossmann, 2012a, 2014b) <br />
    - VR – Vehicle Routing problem (Khaligh & MirHassani, 2016) <br />
    - DSR – Demand-Side Response scheme planning problem (Giannelos et al., 2018) <br />
    - NTIP – New Technology Investment Planning problem (Christian & Cremaschi, 2018) <br />
    - ALIP – Artificial Lift Infrastructure Planning problem (Zeng & Cremaschi, 2022) <br />
    - CPwTL – Capacity Planning with Technology Learning problem (Rathi & Zhang, 2022) <br />
    - CCSEOR – CCS-EOR planning problem (Abdoli et al., 2023)
    
    See the paper cited in the summary section for the complete reference.

4. Select `True` for a complete-recourse added model. Select `False` otherwise.
    ```
    Complete_recourse_added = False 
    ```
    Complete-recourse-added models are available for Size, OPMPSP, PNS, VR, DSR, and ALIP only.

5. Select the instance to run. To view available instance names, navigate to `Parameters` → `Selected model` → `Model_name_Cases` → `Case_data.py`.
    ```
    MD = Instances.instance_name() 
    ```

6. Select the solver (e.g., cplex).
    ```
    sol_select = "solver_name" 
    ```

7. Run the `main.py` file.

## Model
All Models are located in `MSSP` → `Model`.

## ScenarioTreeAnalizer
This tool analyzes the solution by tracking changes in differentiator variable values and provides the following information: <br />
* The time periods when uncertainty is realized (i.e., branching points in the scenario tree) <br />
* Indistinguishable scenario subsets before and after each uncertainty realization <br />
* The maximum number of stages <br />
* The total number of uncertainty realizations <br />

The results are saved as a file named `ModelName_realization_MSSP_InstanceName
`<br />
This file is located under `Solutions_MSSP` → `selected model` → `selected run` <br />
To use the analysis tool, the following inputs are needed:

### 1. Differentiator variable information <br />

**Example (Size problem)**
```
DF = {model_MSSP.z_its:{'t_index':1,'s_index':2,'sets':(I,T,S),'trigger_GT':0.8}} 
```
- `model_MSSP.z_its`: Differentiator variable <br />
- `'t_index'`: Time index position<br />
- `'s_index'`: Scenario index position <br />
- `'sets'`: All index sets <br />
- `'trigger_GT'`: Threshold — if the variable value is Greater Than this threshold, uncertainty is realized <br />
- `'trigger_LT'`: Threshold — if the variable value is Less Than this threshold, uncertainty is realized

**Notes:**  <br />
The differentiator variable `model_MSSP.z_its` ($z_{i,t,s} \in\{0,1\}$) has three indices: $i$, $t$, and $s$. The time index $t$ and scenario index $s$ correspond to the second and third positions, which in Python's zero-based indexing are positions `1` and `2`, respectively. <br />
Uncertainty realizations are identified based on changes in the values of differentiator variables. In this example, $z_{i,t,s}$ switches from 0 to 1 when an uncertainty realization occurs. To capture the uncertainty realization correctly, the `'trigger_GT'` value must be set between 0 and 1 (i.e., $0 <$ `'trigger_GT'` $< 1$). 

### 2. Uncertain parameter information <br />

**2.1 Endogenous uncertainty**

**Example (Size problem)**
```
Endo_input = ({'param':model_MSSP.Cpr_is,'s_index':1, 'Differentiator':{'variable':model_MSSP.z_its,'diff_set':D_ssp,'diff_index':(0,)}},) 
```
- `'param'`: Endogenous uncertain parameter <br />
- `'s_index'`: Scenario index position <br />
- `'variable'`: Corresponding differentiator variable <br />
- `'diff_set'`: Corresponding differentiator set <br />
- `'diff_index'`: Index position of the endogenous uncertainty source

**Notes:**  <br />
The endogenous uncertain parameter is the unit production cost `model_MSSP.Cpr_its` ($C^{pr}_{i,s}$), which has indices $i$ and $s$. The scenario index $s$ is the second index, so its position is `1` in Python’s zero-based indexing. <br /> 
`'variable'` specifies the differentiator variable associated with this uncertain parameter. In this case, the differentiator variable is `model_MSSP.z_its` ($z_{i,t,s} \in\{0,1\}$). The unit production cost for size $i$ in scenario $s$ is realized when $z_{i,t,s}$ changes from 0 to 1 (i.e., when size $i$ is produced in scenario $s$). <br />
`'diff_set'` specifies the differentiator set associated with this uncertain parameter. In this example, the differentiator set is `D_ssp`, defined as $\mathcal{D}(s,s')=\{i \in \mathcal{I} \mid C^{pr}_{i,s} \neq C^{pr}_{i,s'}\}$, where $\mathcal{I}$ denotes the set of sizes. <br />
`'diff_index'` specifies the index position of the endogenous uncertainty source for the differentiator variable. In this example, the first index $i$ of $z_{i,t,s} \in\{0,1\}$ is the only endogenous uncertainty source. The input is provided as a tuple `(0,)` because multiple sources may exist in other models. 

For additional examples, refer to the problem-specific settings in the `main.py` file.

**2.2 Exogenous uncertainty**

**Example (Size problem)**
```
Exo_input = ({'param':model_MSSP.D_its,'t_index':1,'s_index':2},)
```
- `'param'`: Exogenous uncertain parameter <br />
- `'t_index'`: Time index position <br />
- `'s_index'`: Scenario index position <br />

**Notes:**  <br />
The exogenous uncertain parameter is the demand `model_MSSP.D_its` ($D_{i,t,s}$), which has indices $i$, $t$, and $s$. The time index $t$ and scenario index $s$ are the second and third indices, corresponding to positions `1` and `2` in Python's zero-based indexing. <br /> 

## Solution
The outputs — including objective function values, solution time, variable values, and information structure — are stored in the `Solutions_MSSP` folder. <br />
To specify which variables values to save, define them as follows.
 
**Example (Size problem)**
```
Var_output = {model_MSSP.z_its, model_MSSP.y_its, model_MSSP.x_ijts, model_MSSP.w_its}
```

In this example, the values of `model_MSSP.z_its` ($z_{i,t,s}$), `model_MSSP.y_its` ($y_{i,t,s}$), `model_MSSP.x_ijts` ($x_{i,j,t,s}$), and `model_MSSP.w_its` ($w_{i,t,s}$) are written to output files.

## Contact
For any questions, feel free to email szc0113@auburn.edu
