import matplotlib.pyplot as plt
import pandas as pd

ha_to_m2 = 1e4


def plot_SNOMIN_parameters(Thickness, CNRatioSOMI, CRAIRC, FSOMI, RHOD, Soil_pH):
    fig, axs = plt.subplots(2,3, layout = "constrained", figsize=(12,6))
    x = [None] * len(Thickness)
    x_centroid = [None] * len(Thickness)
    for i in range(0, len(x_centroid)):
        if(i == 0):
            x[i] = Thickness[i]
            x_centroid[i] = x[i] / 2
        else:
            x[i] = x[i-1] + Thickness[i]
            x_centroid[i] = x[i - 1] + Thickness[i]/2

    axs[0, 0].plot([0] + x_centroid + [120.], [CNRatioSOMI[0]] + CNRatioSOMI + [CNRatioSOMI[-1]], "o-")
    axs[0, 0].set_xlim(0, 130)
    axs[0, 0].set_ylim(0, 30)
    axs[0, 0].set_xlabel("Depth (cm)")
    axs[0, 0].set_ylabel("C:N ratio of organic matter\n" + r"(kg C $\mathrm{kg}^{-1}$ N)")

    axs[0, 1].plot([0] + x_centroid + [120.], [CRAIRC[0]] + CRAIRC + [CRAIRC[-1]], "o-")
    axs[0, 1].set_xlim(0, 130)
    axs[0, 1].set_ylim(0, 0.1)
    axs[0, 1].set_xlabel("Depth (cm)")
    axs[0, 1].set_ylabel("Critical air content\n" + r"($\mathrm{m}^{3}$ air $\mathrm{m}^{-3}$ soil)")

    axs[0, 2].plot([0] + x_centroid + [120.], [FSOMI[0]] + FSOMI + [FSOMI[-1]], "o-")
    axs[0, 2].set_xlim(0, 130)
    axs[0, 2].set_ylim(0, 0.1)
    axs[0, 2].set_xlabel("Depth (cm)")
    axs[0, 2].set_ylabel("Fraction of organic matter\n" + r"(kg OM $\mathrm{kg}^{-1}$ soil)")

    axs[1, 0].plot([0] + x_centroid + [120.], [RHOD[0]] + RHOD + [RHOD[-1]], "o-")
    axs[1, 0].set_xlim(0, 130)
    axs[1, 0].set_ylim(0, 2.0)
    axs[1, 0].set_xlabel("Depth (cm)")
    axs[1, 0].set_ylabel("Soil bulk density\n" + r"($\mathrm{kg}$ soil $\mathrm{m}^{-3}$ soil)")

    axs[1, 1].plot([0] + x_centroid + [120.], [Soil_pH[0]] + Soil_pH + [Soil_pH[-1]], "o-")
    axs[1, 1].set_xlim(0, 130)
    axs[1, 1].set_ylim(0, 7.0)
    axs[1, 1].set_xlabel("Depth (cm)")
    axs[1, 1].set_ylabel("Soil pH\n" + r"log(mol $\mathrm{H}^{+}$ $\mathrm{L}^{-1}$)")
    return fig
    
    
def plot_pF_vs_soilmoisture(SMfromPFs, Thickness, pFs):
    fig, axs = plt.subplots(1,len(Thickness), layout = "constrained")
    fig.set_figheight(5)
    fig.set_figwidth(15)
    zmin = 0.

    for i in range(0, len(Thickness)):
        zmax = zmin + Thickness[i]
        pFs = [None] * len(pFs)
        SMs = [None] * len(pFs)
        for j in range(0, len(pFs)):
            pFs[j] = SMfromPFs[i][int(j * 2)]
            SMs[j] = SMfromPFs[i][int(j * 2 + 1)]
        axs[i].plot(pFs, SMs, "-o")
        axs[i].set_xlabel("pF\n" + r"log(cm $\mathrm{H}_{2}\mathrm{O}$)")
        axs[i].set_ylabel("Soil moisture content\n" + r"($\mathrm{cm}^{3}$ $\mathrm{H}_{2}\mathrm{O}$ $\mathrm{cm}^{-3}$ soil)")
        axs[i].set_title(f"{round(zmin)}-{round(zmax)} cm")
        axs[i].set_xlim(0, 6)
        axs[i].set_ylim(0., 0.50)    
        zmin = zmax

    return fig


def plot_pF_vs_conductivity(CONDfromPFs, Thickness, pFs):
    fig, axs = plt.subplots(1,len(Thickness), layout = "tight")
    fig.set_figheight(5)
    fig.set_figwidth(15)
    zmin = 0.
    for i in range(0, len(Thickness)):
        zmax = zmin + Thickness[i]
        pFs = [None] * len(pFs)
        CONDs = [None] * len(pFs)
        for j in range(0, len(pFs)):
            pFs[j] = CONDfromPFs[i][int(j * 2)]
            CONDs[j] = CONDfromPFs[i][int(j * 2 + 1)]
        axs[i].plot(pFs, CONDs, "o-")
        axs[i].set_xlabel("pF\n" + r"log(cm $\mathrm{H}_{2}\mathrm{O}$)")
        axs[i].set_ylabel("10-base log hydr. conductivity\n" + r"$\mathrm{log}(\mathrm{cm}$ $\mathrm{H}_{2}\mathrm{O}$ $\mathrm{s}^{-1})$")
        axs[i].set_title(f"{round(zmin)}-{round(zmax)} cm")
        axs[i].set_xlim(0, 6)
        axs[i].set_ylim(-40, 10)
        zmin = zmax
    return fig


def plot_w72_variables(df_output):
    import datetime as dt
    sowing_date = df_output.day[df_output.DVS == -0.1].iloc[0]
    df_output["DAS"] = df_output.apply(lambda x: (x.day - sowing_date).days, axis = 1)    
    kg_to_Mg = 1e-3
    df_output["tdm"] = df_output.WST + df_output.WRT + df_output.WSO + df_output.WLV

    fig, axs = plt.subplots(1,3, layout="constrained")
    fig.set_figheight(5)
    fig.set_figwidth(15)

    axs[0].set_xlabel("Days after sowing")
    axs[0].set_ylabel("Total dry matter\n" + r"($\mathrm{Mg}$ DM $\mathrm{ha}^{-1}$)")
    axs[0].set_xlim(0, df_output["DAS"].max())
    axs[0].set_ylim(0, 25)
    axs[0].plot(df_output.DAS, df_output.tdm * kg_to_Mg)

    axs[1].set_xlabel("Days after sowing")
    axs[1].set_ylabel("Leaf area index\n" + r"($\mathrm{m}^{2}$ $\mathrm{m}^{-2}$)")
    axs[0].set_xlim(0, df_output["DAS"].max())    
    axs[1].set_ylim(0, 10)
    axs[1].plot(df_output.DAS, df_output.LAI)

    axs[2].set_xlabel("Days after sowing")
    axs[0].set_xlim(0, df_output["DAS"].max())    
    axs[2].set_ylabel("Grain dry matter\n" + r"($\mathrm{Mg}$ DM $\mathrm{ha}^{-1}$)")
    axs[2].set_ylim(0, 25)
    axs[2].plot(df_output.DAS, df_output.WSO * kg_to_Mg )    
    return fig

def plot_w81_soil_variables(df_output, Thickness):
    dict_soilstate = {}
    number_of_simulated_days = len(df_output)
    number_of_layers = len(df_output.NH4.iloc[0])

    # Define lists to contain layer specific amounts of NH4-N, amounts of NO3-N and soil moisture contents
    for j in range(0, number_of_layers):
        dict_soilstate[f"NH4_{j+1}"] = []
        dict_soilstate[f"NO3_{j+1}"] = []
        dict_soilstate[f"SM_{j+1}"] = []

    # Store daily, layer-specific values of the amounts of NH4-N, amounts of NO3-N and soil moisture contents
    for i in range(0, number_of_simulated_days):
        for j in range(0, number_of_layers):
            dict_soilstate[f"NH4_{j+1}"].append(df_output.NH4.iloc[i][j])
            dict_soilstate[f"NO3_{j+1}"].append(df_output.NO3.iloc[i][j])
            dict_soilstate[f"SM_{j+1}"].append(df_output.SM.iloc[i][j])

    # Add layer specific values to dataframe
    for j in range(0, number_of_layers):
        df_output[f"NH4_{j+1}"] = dict_soilstate[f"NH4_{j+1}"]
        df_output[f"NO3_{j+1}"] = dict_soilstate[f"NO3_{j+1}"]
        df_output[f"SM_{j+1}"] = dict_soilstate[f"SM_{j+1}"]

    fig, axs = plt.subplots(3, number_of_layers, layout = "tight")
    fig.set_figheight(15)
    fig.set_figwidth(25)

    for j in range(0, number_of_layers):    
        axs[0,j].plot(df_output.DOY, df_output[f"NH4_{j+1}"] * ha_to_m2)
        axs[0,j].set_xticks([])
        axs[0,j].set_ylim(0, 200)
        axs[1,j].plot(df_output.DOY, df_output[f"NO3_{j+1}"] * ha_to_m2)
        axs[1,j].set_ylim(0, 200)
        axs[1,j].set_xticks([])
        axs[2,j].set_xlabel("Day of year", fontsize = 20)    
        axs[2,j].plot(df_output.DOY, df_output[f"SM_{j+1}"])    
        axs[2,j].set_ylim(0, 0.4)
        axs[2,j].tick_params(axis='x', labelsize=20)
        
        if(j > 0):
            axs[0,j].set_yticks([])
            axs[1,j].set_yticks([])
            axs[2,j].set_yticks([])
    zmin = 0.
    for i in range(0, number_of_layers):
        zmax = zmin + Thickness[i]
        axs[0,i].set_title(f"{round(zmin)}-{round(zmax)} cm", fontsize = 20) 
        zmin = zmax
    axs[0,0].set_ylabel("$\rm {NH}_4^{+}$-$\rm {N}$ amount\n" + r"($\rm {kg}$ $\rm {NH}_4^{+}$-$\rm {N}$ $\rm {ha}^{-1}$)", fontsize = 20)
    axs[1,0].set_ylabel("$\rm {NO}_3^{-}$-$\rm {N}$ amount\n" + r"($\rm {kg}$ $\rm {NO}_3^{-}$-$\rm {N}$ $\rm {ha}^{-1}$)", fontsize = 20)
    axs[0,0].tick_params(axis='y', labelsize=20)
    axs[1,0].tick_params(axis='y', labelsize=20)
    axs[2,0].tick_params(axis='y', labelsize=20)    
    return fig
    

def plot_w81_crop_variables(df_output):
    sowing_date = df_output.day[df_output.DVS == -0.1].iloc[0]
    df_output["DAS"] = df_output.apply(lambda x: (x.day - sowing_date).days, axis = 1)    
    
    fig, axs = plt.subplots(1,3, layout="constrained")
    fig.set_figheight(5)
    fig.set_figwidth(15)

    df_output["NamountTot"] = df_output.NamountLV + df_output.NamountST + df_output.NamountRT + df_output.NamountSO

    axs[0].set_xlabel("Days after sowing")
    axs[0].set_ylabel("Crop N amount" + r"($\rm {kg} N$ $\rm {ha}^{-1}$)")
    axs[0].set_ylim(0, 350)
    axs[0].plot(df_output.DAS, df_output.NamountTot )

    axs[1].set_xlabel("Days after sowing")
    axs[1].set_ylabel("Leaf N amount\n" + r"($\rm {kg}$ N $\rm {ha}^{-1}$)")
    axs[1].set_ylim(0, 350)
    axs[1].plot(df_output.DAS, df_output.NamountLV )

    axs[2].set_xlabel("Days after sowing")
    axs[2].set_ylabel("Grain N amount\n" + r"($\rm {kg}$ N $\rm {ha}^{-1}$)")
    axs[2].set_ylim(0, 350)
    axs[2].plot(df_output.DAS, df_output.NamountSO)    
    return fig
    
    
def plot_w81_soil_totals(df_output, Thickness, number_of_layers):
    import datetime as dt
    sowing_date = df_output.day[df_output.DVS == -0.1].iloc[0]
    df_output["DAS"] = df_output.apply(lambda x: (x.day - sowing_date).days, axis = 1)      
    df_output["NH4N_tot"] = 0.
    df_output["NO3N_tot"] = 0.
    df_output["H2O_tot"] = 0.
    for i in range(len(df_output)):
        for j in range(len(Thickness)):
            df_output.loc[i, "NH4N_tot"] += df_output.loc[i, "NH4"][j]
            df_output.loc[i, "NO3N_tot"] += df_output.copy().NO3.iloc[i][j]
            df_output.loc[i, "H2O_tot", ] += df_output.copy().SM.iloc[i][j] * Thickness[j]
    fig, axs = plt.subplots(1,3, layout = "constrained")
    fig.set_figheight(5)
    fig.set_figwidth(15)
    axs[0].plot(df_output["DAS"], df_output.NH4N_tot * ha_to_m2)
    axs[0].set_xlabel("Day after sowing", fontsize=15)
    axs[0].set_ylabel("Total amount of ${\mathrm{NH}_4}^{+}$-$\mathrm{N}$\n" + r"($\mathrm{kg}$ ${\mathrm{NH}_4}^{-}$-$\mathrm{N}$  $\mathrm{ha}^{-1}$)", fontsize=15)
    axs[0].set_ylim(0,100)
    axs[1].plot(df_output["DAS"], df_output.NO3N_tot * ha_to_m2)
    axs[1].set_xlabel("Day after sowing", fontsize=15)
    axs[1].set_ylabel("Total amount of ${\mathrm{NO}_3}^{-}$-$\mathrm{N}$\n" + r"($\mathrm{kg}$ ${\mathrm{NO}_3}^{-}$-$\mathrm{N}$  $\mathrm{ha}^{-1}$)", fontsize=15)
    axs[1].set_ylim(0,100)
    axs[2].plot(df_output["DAS"], df_output.H2O_tot)
    axs[2].set_xlabel("Day after sowing")
    axs[2].set_ylabel("Total amount of ${\mathrm{H}_2}\mathrm{O}$\n" + r"(cm $\mathrm{H}_2\mathrm{O})$", fontsize=15)
    axs[2].set_ylim(0,60)
    axs[0].tick_params(axis='x', labelsize=15)
    axs[1].tick_params(axis='x', labelsize=15)
    axs[2].tick_params(axis='x', labelsize=15)
    axs[0].tick_params(axis='y', labelsize=15)
    axs[1].tick_params(axis='y', labelsize=15)
    axs[2].tick_params(axis='y', labelsize=15)
    return fig
