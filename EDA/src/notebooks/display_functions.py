import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def plot_categorical_distribution(df, cat_cols, relative = False, show_values = False, limit = 10): # Univariable
    '''
    Generates bar charts for the distribution of categorical variables.

    Parameters:
    - df: DataFrame containing the data to be graphed.
    - cat_cols: List of names of the categorical columns in `df` for which the graphs will be generated.
    - relative: If True, the relative frequency of the categories is shown instead of the absolute frequency (default value: False).
    - show_values: If True, shows the numerical values above each bar (default value: False).
    - limit: Maximum number of categories to show in each graph (default value: 10).
    '''
    num_columns = len(cat_cols)
    num_rows = (num_columns // 2) + (num_columns % 2)

    fig, axes = plt.subplots(num_rows, 2, figsize=(20, 5 * num_rows))
    axes = axes.flatten() 

    for i, col in enumerate(cat_cols):
        ax = axes[i]
        if relative:
            total = df[col].value_counts().sum()
            serie = df[col].value_counts().nlargest(limit).apply(lambda x: x / total)
            sns.barplot(x = serie.index, y = serie, ax = ax, palette = 'viridis', hue = serie.index, legend = False)
            ax.set_ylabel('Relative Frequency')
            # Find the maximum value and set the upper limit of the y-axis.
            max_value = serie.max()
            upper_limit = max_value + 0.1
            ax.set_ylim(top = upper_limit)
        else:
            serie = df[col].value_counts().nlargest(limit)
            sns.barplot(x = serie.index, y = serie, ax = ax, palette = 'viridis', hue = serie.index, legend = False)
            ax.set_ylabel('Frequency')
            # Find the maximum value and set the upper limit of the y-axis.
            max_value = serie.max()
            upper_limit = max_value + 1000
            ax.set_ylim(top = upper_limit)

        ax.set_title(f'Distribution of {col}')
        ax.set_xlabel('')
        ax.tick_params(axis = 'x', rotation = 45)

        if show_values:
            for p in ax.patches:
                height = p.get_height()
                ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2., height),
                            ha = 'center', va = 'center', xytext = (0, 9), textcoords = 'offset points')

    for j in range(i + 1, num_rows * 2):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()


def plot_combined_graphs(df, columns, whisker_width = 1.5, bins = None): # Univaribale - Numeric
    '''
    Generates combined graphs for the specified columns in a DataFrame.
    For each column that is numeric (type `int64` or `float64`), two types of graphs are generated: Histogram and Boxplot.

    Parameters:
    - df: DataFrame containing the data to be plotted.
    - columns: List of column names in `df` for which the graphs will be generated.
    - whisker_width: Width of the whiskers in the boxplot (default value: 1.5).
    - bins: Number of bins for the histogram (default value: 1.5). 
    '''

    num_cols = len(columns)
    if num_cols:
        
        fig, axes = plt.subplots(num_cols, 2, figsize = (12, 5 * num_cols))
        print(axes.shape)

        for i, column in enumerate(columns):
            if df[column].dtype in ['int64', 'float64']:
                # Histogram and KDE
                sns.histplot(df[column], kde = True, ax = axes[i, 0] if num_cols > 1 else axes[0], bins = "auto" if not bins else bins)
                if num_cols > 1:
                    axes[i, 0].set_title(f'Histogram and KDE of {column}')
                else:
                    axes[0].set_title(f'Histogram and KDE of {column}')

                # Boxplot
                sns.boxplot(x = df[column], ax = axes[i, 1] if num_cols > 1 else axes[1], whis = whisker_width)
                if num_cols > 1:
                    axes[i, 1].set_title(f'Boxplot of {column}')
                else:
                    axes[1].set_title(f'Boxplot of {column}')

        plt.tight_layout()
        plt.show()



def plot_bar_with_values(data, cat_cols, num_col, order_func = None, palette = 'viridis', figsize = (14, 8), title = 'Distribution of {}', xlabel = '', ylabel = ''):
    """
    Creates bar charts with numerical values above each bar for each categorical column in cat_cols.
    The order of the bars is determined by a custom order function, limited to top_n categories.

    Parameters:
    - data: DataFrame with the data.
    - cat_cols: List of column names for the x-axis (categorical columns).
    - y: Name of the column for the y-axis (e.g., 'salary_in_usd').
    - order_func: Function to determine the order of the categories. It should return a list of ordered categories.
    - palette: Palette of colors for the graphs (default is 'viridis').
    - figsize: Size of the figure (default is (14, 8)).
    - title_template: Template for the title of each graph (default is 'Distribution of {}').
    - xlabel: x-axis label (default is '').
    - ylabel: Label of the y-axis (default is '').
    - top_n: Number of top categories to display (default is 11).
    """
    
    # Iterate over each column in cat_cols
    for col in cat_cols:
        plt.figure(figsize = figsize)
        
        # Determinar el orden de las categorías usando la función personalizada
        if order_func:
            order = order_func(data, col, num_col)
        else:
            # Default ordering by frequency if no function is provided
            order = data[col].value_counts().index.tolist()[:10]
        
        ax = sns.barplot(x = col, y = num_col, data = data, errorbar = None, palette = palette, order = order)
        
        # Add numerical values above each bar
        for p in ax.patches:
            height = p.get_height()
            ax.annotate(f'{height:.2f}', (p.get_x() + p.get_width() / 2, height), 
                        ha = 'center', va = 'center', xytext = (0, 10), textcoords = 'offset points', 
                        fontsize = 10, color = 'black')
        
        # Configure axes and title
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        plt.title(title.format(col))
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.show()


def plot_grouped_boxplots(df, cat_cols, num_col):
    '''
    Generates grouped boxplots for a given DataFrame, dividing categorical data into manageable groups for better visualisation. 

    Parameters:
    - df: The DataFrame containing the data to display.
    - cat_cols: List of the categorical columns in the DataFrame.
    - num_col: Name of the numeric column in the DataFrame.
    '''
    for cat_col in cat_cols:
        # Calculate the average wage for each category
        avg_salaries = df.groupby(cat_col)[num_col].mean().sort_values(ascending = False)
        
        # Select the 5 categories with the highest average salaries
        top_5_cats = avg_salaries.head(5).index
        top_5_df = df[df[cat_col].isin(top_5_cats)]
        
        # Get the selected unique categories
        unique_cats = top_5_df[cat_col].unique()
        num_cats = len(unique_cats)
        group_size = 5

        for i in range(0, num_cats, group_size):
            subset_cats = unique_cats[i:i+group_size]
            subset_df = top_5_df[top_5_df[cat_col].isin(subset_cats)]
            
            plt.figure(figsize=(10, 6))
            sns.boxplot(x = cat_col, y = num_col, data = subset_df)
            plt.title(f'Boxplots of {num_col} for {cat_col} (Group {i//group_size + 1})')
            plt.xticks(rotation=45)
            plt.show()