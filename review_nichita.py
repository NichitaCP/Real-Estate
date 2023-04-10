import os
import pandas as pd



def string_replace(string, str_to_replace=None, replace_with=None) -> str:
    """
    Replace the occurrences of a substring in a given string with a replacement string.

    Args:
        string (str): The input string to be processed.
        str_to_replace (str): The substring to be replaced in the input string. If not provided, defaults to None.
        replace_with (str): The replacement string that will be used to replace the occurrences of the substring. If not provided, defaults to None.

    Returns:
        str: The modified string after replacing the occurrences of the substring with the replacement string.

    Example:
    >>> string_replace("hello world", "o", "0")
    'hell0 w0rld'
    >>> string_replace("foo bar baz", "bar", "qux")
    'foo qux baz'
    """
    string = string.replace(str_to_replace, replace_with)
    return string

def read_write(file:str, list_to_replace=None, list_replace_with=None)-> None:
    """
    Read a file, replace the specified substrings in its lines, and overwrite the original file.

    Args:
        file (str): The path to the file to be read and overwritten.
        list_to_replace (list): A list of substrings to be replaced in each line of the file. If not provided, defaults to None.
        list_replace_with (list): A list of replacement strings that will be used to replace the corresponding substrings in the file. If not provided, defaults to None.

    Returns:
        None: The function overwrites the original file and does not return a value.

    Example:
        Suppose the file "example.txt" contains the following lines:
            The quick brown fox jumps over the lazy dog.
            She sells seashells by the seashore.
            Peter Piper picked a peck of pickled peppers.

        >>> read_write("example.txt", ["e", "o"], ["3", "0"])
        # The lines in "example.txt" will be replaced as follows:
        #   The quick br0wn f3x jumps 0v3r th3 lazy d0g.
        #   Sh3 s3lls s3ash3lls by th3 s3ash0r3.
        #   P3t3r Pip3r pick3d a p3ck of pickl3d p3pp3rs.
    """
    with open(file, 'r') as f:
        lines = f.readlines()
    with open(file, 'w') as f:
        for line in lines:
            for tr, rw in zip(list_to_replace, list_replace_with):
                line = string_replace(string=line, str_to_replace=tr, replace_with=rw)
            f.write(line)


def prop_printer(file:str, n_semicolons:int) -> None:
    """
    Prints the proportion of lines in a file that contain a different number of semicolons than n_semicolons.

    Args:
    - file (str): The name of the file to be processed.
    - n_semicolons (int): The number of semicolons to be searched for in each line.

    Returns:
    - None

    Raises:
    - FileNotFoundError: If the specified file is not found.
    - TypeError: If the specified file is not a string or if n_semicolons is not an integer.

    Example:
    >>> prop_printer('my_file.txt', 2)
    Proportion of flagged lines for my_file.txt: 33.33 %
    """
    list_obj = []
    with open(file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.count(';')!=n_semicolons:
            list_obj.append(line)
    print(f"Proportion of flagged lines for {file}: {len(list_obj)/len(lines)*100} %")

def val_inval_lists(file: str, n_semicolons: int) -> tuple[list[str], list[str]]:
    """
    Separates the lines in a file into two lists based on the number of semicolons in each line.

    Args:
    - file (str): The name of the file to be processed.
    - n_semicolons (int): The number of semicolons to be searched for in each line.

    Returns:
    - A tuple of two lists of strings. The first list contains the lines that have the specified number of semicolons,
      while the second list contains the lines that do not have the specified number of semicolons.

    Raises:
    - FileNotFoundError: If the specified file is not found.
    - TypeError: If the specified file is not a string or if n_semicolons is not an integer.

    Example:
    >>> valid_list, invalid_list = val_inval_lists('my_file.txt', 2)
    >>> print(valid_list)
    ['valid line 1;valid line 2;\n', 'valid line 3;valid line 4;\n']
    >>> print(invalid_list)
    ['invalid line 1;\n', 'invalid line 2;\n', 'invalid line 3;\n']
    """
    valid_list = []
    invalid_list = []
    with open(file, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.count(';')== n_semicolons:
            valid_list.append(line)
        else:
            invalid_list.append(line)
    return valid_list, invalid_list

def drop_nonconform_lines(file, n_semicolons:int)->None:
    """
    Drops lines from a file that do not have the specified number of semicolons.

    Args:
    - file (str): The name of the file to be processed.
    - n_semicolons (int): The number of semicolons to be searched for in each line.

    Returns:
    - None

    Raises:
    - FileNotFoundError: If the specified file is not found.
    - TypeError: If the specified file is not a string or if n_semicolons is not an integer.

    Example:
    >>> drop_nonconform_lines('my_file.txt', 2)
    """
    with open(file, 'r') as f:
        lines = f.readlines()
    with open(file, 'w') as f:
        for line in lines:
            if line.count(';')==n_semicolons:
                f.write(line)
                
                
                
chars_to_replace = ['ème', 'è', 'é', '€', 'm²', ' (75)', ' (69)', ' (13)', 'Terrain', 'terrain', 'er']
replace_chars_with_paris = [';', 'e', 'e', 'eur', 'm2', '', '', '', ';']
replace_chars_with = [';', 'e', 'e', 'eur', 'm2;', '', '', '', '','',';']

paris = 'annuaire_paris.txt'
lyon = 'annuaire_lyon.txt'
marseille = 'annuaire_marseille.txt'

read_write(paris, chars_to_replace, replace_chars_with_paris)
read_write(lyon, chars_to_replace, replace_chars_with)
read_write(marseille, chars_to_replace, replace_chars_with)

prop_printer(paris, 2)
prop_printer(lyon, 2)
prop_printer(marseille, 2)



lyon_val, lyon_inval = val_inval_lists(lyon, 2)
lyon_appart_list = []
for i,val in enumerate(lyon_inval):
    if 'appartement' in val:
        lyon_appart_list.append(val)
print(f"The appartments that were flagged as invalid in Lyon file represent \
{100*len(lyon_appart_list)/(len(lyon_val)+len(lyon_inval))}% of the dataset")



marseille_val, marseille_inval = val_inval_lists(marseille, 2)
marseille_appart_list = []
for i,val in enumerate(marseille_inval):
    if 'appartement' in val:
        marseille_appart_list.append(val)
print(f"The appartments that were flagged as invalid in Marseille file represent \
{100*len(marseille_appart_list)/(len(marseille_val)+len(marseille_inval))}% of the dataset")



drop_nonconform_lines(paris, 2)
drop_nonconform_lines(lyon, 2)
drop_nonconform_lines(marseille, 2)
prop_printer(paris, 2)
prop_printer(lyon, 2)
prop_printer(marseille, 2)


df_paris = pd.read_csv(paris, encoding='latin-1', header = None, sep = ';')
df_lyon = pd.read_csv(lyon, encoding='latin-1', header = None, sep = ';')
df_marseille = pd.read_csv(marseille, encoding='latin-1', header = None, sep = ';')
df_final = pd.concat([df_paris, df_marseille, df_lyon], ignore_index=True)
df_final = df_final.rename(columns = {0:'type_logement', 1: 'surface', 2: 'prix'})
app_mask = df_final['type_logement'].str.contains('appartement')
df_app = df_final.copy(deep=True)
df_final = df_final[app_mask]
df_split = df_final.type_logement.str.split(' ', expand = True)
df_split = df_split.rename(columns = {0: 'type_l', 1 : 'ville', 2: 'arr'})
df_final = pd.concat([df_final, df_split], axis = 1)
df = df_final.copy()
df.head()



pattern_pieces = r'(\d+)\s*piece[s]?\s*'
pattern_ch = r'(\d+)\s*chambre[s]?\s*'
df['n_pieces'] = df['surface'].str.extract(pattern_pieces, expand = False).astype(float)
df['n_pieces'] = df['n_pieces'].fillna(0)
df['n_chambres'] = df['surface'].str.extract(pattern_ch, expand = False).astype(float)
df['n_chambres'] = df.n_chambres.fillna(0)

df['n_chambres'].value_counts(dropna=False, normalize=True)



df['n_pieces'].value_counts(dropna=False, normalize=True)



df['surface_m2'] = df['surface'].str.replace(pattern_pieces, '', regex=True)
df['surface_m2'] = df['surface_m2'].str.replace(pattern_ch, '',regex = True)
df['surface_m2'] = df['surface_m2'].str.replace('m2','',regex=True).str.strip()
df['surface_m2'] = pd.to_numeric(df['surface_m2'], errors = 'coerce')
nn_rows = df[pd.to_numeric(df['surface_m2'], errors = 'coerce').isna()]
nn_rows



df['prix'] = df['prix'].str.replace('eur| ', '', regex=True).str.strip()
df['prix'] = pd.to_numeric(df['prix'], errors='coerce')
df = df.dropna(subset=['prix', 'surface_m2'])
cols = ["type_l", "ville", "arr", "n_pieces", "n_chambres", "surface_m2", "prix"]
df_pml = df.loc[:, cols]
df_pml['prix_m2'] = df['prix'] // df['surface_m2']
df_pml['arr'] = df_pml.arr.astype('int')
df_pml.groupby(['ville', 'arr'])[['prix_m2','surface_m2']].mean()
q1_pmc, q2_pmc, q3_pmc, q4_pmc = df_pml['prix_m2'].quantile([0.25, 0.5, 0.75, 1])
q1_prix, q2_prix, q3_prix, q4_prix = df_pml['prix'].quantile([0.25, 0.5, 0.75, 1])
iqr_pmc = q3_pmc - q1_pmc
iqr_prix = q3_prix - q1_prix
lower_prix = q1_prix- 3*iqr_prix
upper_prix = q3_prix + 3*iqr_prix
lower_pmc = q1_pmc - 1.5*iqr_pmc
upper_pmc = q3_pmc + 1.5*iqr_pmc
df_pml[['prix_m2', 'surface_m2']].describe()
df_pml['n_pieces'] = df_pml['n_pieces'].astype('category')


cwd = os.getcwd()
filename = "real_estate_PML.csv"
filepath = os.path.join(cwd, filename)
df_pml.to_csv(filepath, index = False)