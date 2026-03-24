###correlaciones ###

SF = data[data["Site"]=="SFNu"] #I want to see the relationship with nutrients. #HELP: Treatments not analyzed.
columnas = [iWUE, name18O  ,"C (mg/g)","N (mg/g)","P (mg/g)","Al (mg/g)","Ca (mg/g)","Fe (mg/g)","K (mg/g)","Mg (mg/g)","Na (mg/g)","S (mg/g)","Narea"]
df = SF[columnas] # most import to have the df clean only with numeric for the correlation maps.

def corr_pvalue(df):
 
 import textwrap
 from scipy.stats import pearsonr
 from scipy.stats import spearmanr
 from scipy.stats import kendalltau
 import numpy as np
 # Generate the correlation matrix afresh
 corr = df.corr(numeric_only=True)

 # mask the correlation matrix to diagonal
 mask = np.zeros_like(corr, dtype=bool)
 mask[np.triu_indices_from(mask)] = True
 np.fill_diagonal(mask, False)

 fix,ax = plt.subplots(figsize=(10,5))
 plt.title("Correlation map with P-value", fontsize=14)

 # Generate heatmap
 heatmap = sns.heatmap(corr,
                      annot= True,
                      annot_kws={"fontsize": 10},
                      fmt='.2f',
                      linewidths=0.5,
                      cmap='RdBu',
                      mask=mask,
                      ax=ax)

 # calculate and format p-values
 p_values = np.full((corr.shape[0], corr.shape[1]), np.nan)
 for i in range(corr.shape[0]):
  for j in range(i+1, corr.shape[1]):
    x = df.iloc[:, i]
    y = df.iloc[:, j]
    mask = ~np.logical_or(np.isnan(x), np.isnan(y))
    if np.sum(mask) > 0:
      p_values[i, j] = pearsonr(x[mask], y[mask])[1] #change to pearsonr or spearmanr, kendalltau

 # Create a dataframe object for p_values
 p_values = pd.DataFrame(p_values, columns=corr.columns, index=corr.index)

 # Mask the p values
 mask_pvalues = np.triu(np.ones_like(p_values), k=1)

 # Generate maximum and minimum correlation coefficients for p-value annotation color
 max_corr = np.max(corr.max())
 min_corr = np.min(corr.min())

 # Assign p-value annotations, include asterisks for significance
 for i in range (p_values.shape[0]):
  for j in range(p_values.shape[1]):
    if mask_pvalues[i, j]:
      p_value = p_values.iloc[i, j]
      if not np.isnan(p_value):
        correlation_value = corr.iloc[i, j]
        text_color = 'white' if correlation_value >= (max_corr - 0.4) or correlation_value <= (min_corr + 0.4) else 'black'
        if p_value <= 0.01:
            #include double asterisks for p-value <= 0.01
            ax.text(i + 0.5, j + 0.8, f'(p = {p_value:.2f})**',
                    horizontalalignment='center',
                    verticalalignment='center',
                    fontsize=6,
                    color=text_color)
        elif p_value <= 0.05:
            #include single asterisk for p-value <= 0.05
            ax.text(i + 0.5, j + 0.8, f'(p = {p_value:.2f})*',
                    horizontalalignment='center',
                    verticalalignment='center',
                    fontsize=6,
                    color=text_color)
        else:
            ax.text(i + 0.5, j + 0.8, f'(p = {p_value:.2f})',
                    horizontalalignment='center',
                    verticalalignment='center',
                    fontsize=6,
                    color=text_color)

 # Customize x-axis labels
 x_labels = [textwrap.fill(label.get_text(), 13) for label in ax.get_xticklabels()]
 ax.set_xticklabels(x_labels, rotation=45, ha="center")

 # Customize y-axis labels
 y_labels = [textwrap.fill(label.get_text(), 13) for label in ax.get_yticklabels()]
 ax.set_yticklabels(y_labels, rotation=0, ha="right")

 # Display the plot
 return plt.show()

corr_pvalue(df)