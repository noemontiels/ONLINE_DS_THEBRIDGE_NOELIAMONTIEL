import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def plot_categorical_distribution(df, cat_cols, relative = False, show_values = False, limit = 10, palette = 'viridis'): # Univariable
    '''
    Generates bar charts for the distribution of categorical variables.

    Parameters:
    - df: DataFrame containing the data to be plotted.
    - cat_cols: List of names of the categorical columns in `df` for which the graphs will be generated.
    - relative: If True, the relative frequency of the categories is shown instead of the absolute frequency (default value: False).
    - show_values: If True, shows the numerical values above each bar (default value: False).
    - limit: Maximum number of categories to show in each graph (default value: 10).
    - palette: Palette of colors for the graphs (default is 'viridis').
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
            sns.barplot(x = serie.index, y = serie, ax = ax, palette = palette, hue = serie.index, legend = False)
            ax.set_ylabel('Relative Frequency')
            # Find the maximum value and set the upper limit of the y-axis.
            max_value = serie.max()
            upper_limit = max_value + 0.1
            ax.set_ylim(top = upper_limit)
        else:
            serie = df[col].value_counts().nlargest(limit)
            sns.barplot(x = serie.index, y = serie, ax = ax, palette = palette, hue = serie.index, legend = False)
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
    - columns: List of column names in 'df' for which the graphs will be generated.
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
    - data: DataFrame containing the data to be plotted.
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
    - df: DataFrame containing the data to be plotted.
    - cat_cols: List of the categorical columns in the DataFrame.
    - num_col: Name of the numeric column in the DataFrame.
    '''
    for cat_col in cat_cols:
        # Calculate the average wage for each category
        avg_salaries = df.groupby(cat_col)[num_col].mean().sort_values(ascending = False)
        
        # Select the 5 categories with the highest average salaries
        top_10_cats = avg_salaries.head(10).index
        top_10_df = df[df[cat_col].isin(top_10_cats)]
        
        # Get the selected unique categories
        unique_cats = top_10_df[cat_col].unique()
        num_cats = len(unique_cats)
        group_size = 10

        for i in range(0, num_cats, group_size):
            subset_cats = unique_cats[i:i+group_size]
            subset_df = top_10_df[top_10_df[cat_col].isin(subset_cats)]
            
            plt.figure(figsize = (20, 15))
            sns.boxplot(x = cat_col, y = num_col, data = subset_df, palette = 'Set1')
            plt.title(f'Boxplots of {num_col} for {cat_col} (Group {i//group_size + 1})')
            plt.xticks(rotation = 45)
            plt.show()


def plot_categorical_relationship_fin(df, cat_col1, cat_col2, relative_freq = False, show_values = False, size_group = 5, palette = 'viridis'):
    '''
    Generates bar charts to show the relationship between categorical columns.
    Iterates over a list of categorical columns, generating graphs for each possible pair of columns.

    Parameters:
    - df: DataFrame containing the data to be plotted.
    - cat_cols: List of categorical column names in the DataFrame.
    - relative_freq: If True, converts counts to relative frequencies.
    - show_values: If True, shows numeric values above the bars.
    - size_group: Size of the group of categories to display in each chart.
    - palette: Palette of colors for the graphs (default is 'viridis').
    '''
    # Prepare data
    count_data = df.groupby([cat_col1, cat_col2]).size().reset_index(name = 'count')
    total_counts = df[cat_col1].value_counts() 

    # Converts to relative frequencies if requested
    if relative_freq:
        count_data['count'] = count_data.apply(lambda x: x['count'] / total_counts[x[cat_col1]], axis = 1)

    # If there are more than size_group categories in cat_col1, split them into groups of size_group
    unique_categories = df[cat_col1].unique()
    if len(unique_categories) > size_group:
        num_plots = int(np.ceil(len(unique_categories) / size_group))

        for i in range(num_plots):
            # Selects a subset of categories for each chart
            categories_subset = unique_categories[i * size_group:(i + 1) * size_group]
            data_subset = count_data[count_data[cat_col1].isin(categories_subset)]

            # Create the chart
            plt.figure(figsize=(20, 6))
            ax = sns.barplot(x = cat_col1, y = 'count', hue = cat_col2, data = data_subset, order = categories_subset, palette = palette)

            # Add titles and tags
            plt.title(f'Relationship between {cat_col1} and {cat_col2} - Group {i + 1}')
            plt.xlabel(cat_col1)
            plt.ylabel('Frequency' if relative_freq else 'Count')
            plt.xticks(rotation = 45)

            # Show values on the graph
            if show_values:
                for p in ax.patches:
                    ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha = 'center', va = 'center', fontsize = 10, color = 'black', xytext = (0, size_group),
                                textcoords = 'offset points')

            # Show the graph
            plt.show()
    else:
        # Create the chart for less than size_group categories
        plt.figure(figsize = (20, 6))
        ax = sns.barplot(x = cat_col1, y = 'count', hue = cat_col2, data = count_data, palette = palette)

        # Add titles and tags
        plt.title(f'Relationship between {cat_col1} y {cat_col2}')
        plt.xlabel(cat_col1)
        plt.ylabel('Frequency' if relative_freq else 'Count')
        plt.xticks(rotation = 45)

        # Show values on the graph
        if show_values:
            for p in ax.patches:
                ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha = 'center', va = 'center', fontsize = 10, color = 'black', xytext = (0, size_group),
                            textcoords = 'offset points')

        # Show the graph
        plt.show()


def plot_categorical_numerical_relationship(df, categorical_col, numerical_col, show_values = False, measure = 'mean'):
    '''
    Visualises the relationship between a categorical column and a numeric column of a DataFrame,
    using a bar chart.

    Parameters:
    - df: DataFrame containing the data to be plotted.
    - categorical_col: Categorical column name in the DataFrame.
    - numerical_col: Numeric column name in the DataFrame.
    - show_values: If True, shows numeric values above the bars.
    - measure: Specifies the measure of central tendency to be calculated. Can be 'mean' or 'median'. The default value is 'mean'.
    '''    
    # Calculates measure of central tendency (mean or median)
    if measure == 'median':
        grouped_data = df.groupby(categorical_col)[numerical_col].median()
    else:
        # By default, it uses the mean
        grouped_data = df.groupby(categorical_col)[numerical_col].mean()

    # Sort the values
    grouped_data = grouped_data.sort_values(ascending=False)

    # If there are more than 10 categories, divide them into groups of 10.
    if grouped_data.shape[0] > 10:
        unique_categories = grouped_data.index.unique()
        num_plots = int(np.ceil(len(unique_categories) / 10))

        for i in range(num_plots):
            # Selects a subset of categories for each chart
            categories_subset = unique_categories[i * 10:(i + 1) * 10]
            data_subset = grouped_data.loc[categories_subset]

            # Create the chart
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(x = data_subset.index, y = data_subset.values)

            # Add titles and tags
            plt.title(f'Relationship between {categorical_col} and {numerical_col} - Group {i + 1}')
            plt.xlabel(categorical_col)
            plt.ylabel(f'{measure.capitalize()} of {numerical_col}')
            plt.xticks(rotation = 45)

            # Show values on the graph
            if show_values:
                for p in ax.patches:
                    ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                                ha = 'center', va = 'center', fontsize = 10, color = 'black', xytext = (0, 5),
                                textcoords = 'offset points')

            # Show the graph
            plt.show()
    else:
        # Create the chart for less than 10 categories
        plt.figure(figsize = (10, 6))
        ax = sns.barplot(x = grouped_data.index, y = grouped_data.values)

        # Add titles and tags
        plt.title(f'Relationship between {categorical_col} and {numerical_col}')
        plt.xlabel(categorical_col)
        plt.ylabel(f'{measure.capitalize()} of {numerical_col}')
        plt.xticks(rotation = 45)

        # Show values on the graph
        if show_values:
            for p in ax.patches:
                ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                            ha = 'center', va = 'center', fontsize = 10, color = 'black', xytext = (0, 5),
                            textcoords = 'offset points')

        # Show the graph
        plt.show()


def scatterplot_with_correlation(df, column_x, column_y, dot_size = 50, show_correlation = False):
    """
    Creates a scatter plot between two columns and optionally displays the correlation.

    Args:
    - df: DataFrame containing the data to be plotted.
    - column_x: Name of the column for the X axis.
    - column_y: Name of the column for the Y axis.
    - dot_size: Size of the points in the chart. Default is 50.
    - show_correlation: If True, shows the correlation in the chart. Default is False.
    """

    plt.figure(figsize = (10, 6))
    sns.scatterplot(data = df, x = column_x, y = column_y, s = dot_size)

    if show_correlation:
        correlation = df[[column_x, column_y]].corr().iloc[0, 1]
        plt.title(f'Scatterplot with correlation: {correlation:.2f}')
    else:
        plt.title('Scatterplot')

    plt.grid(True)
    plt.show()
