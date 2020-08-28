#------------------------------------------#
# Title: Assignment07.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# KSorge-Toomey, 2020-Aug-19, Turned some tasks from while loops into functions within the appropriate class, Added docstrings
# Ksorge-Toomey, 2020-Aug-26, Added exception handling
# KSorge-Toomey, 2020-Aug-27, Changed to save as binary file
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
strBinaryName = 'CDInventory.dat' # data storage binary file
objFile = None  # file object


# -- PROCESSING -- #

class DataProcessor:
    """Handling data in memory"""
    
    @staticmethod
    def add_user_data(cd_id, cd_title, cd_artist, table):    
        """Function to receive new entry data held in memory
        
        Args:
            cd_id (int): entry id added by user
            cd_title (string): name of cd title added by user
            cd_artist (sting): name of cd artist added by user
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
        
        Returns:
            None.
        """
        intID = int(cd_id)
        dicRow = {'ID': intID, 'Title': cd_title, 'Artist': cd_artist}
        table.append(dicRow)
        
        
    @staticmethod
    def delete_entry(id_to_remove, table):
        """Function to delete entry chosen by ID number
        
        Args:
            id_to_remove (int): entry id to delete
            table (list of dict): 2d data structure (lists of dicts) that hold the data during runtime
        
        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:   
            intRowNr += 1
            if row['ID'] == id_to_remove:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')


class FileProcessor:
    """Processing the data to and from binary file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        try:
            objFile = open(file_name, 'r')
        except FileNotFoundError as e:
            print('\nFile not found.')
            print(e)
        else:
            for line in objFile:
                data = line.strip().split(',')
                dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
                table.append(dicRow)
            objFile.close()

    @staticmethod
    def write_file(file_name):
        """Function to create CDInventory.txt if file does not already exist
        
        Args:
            file_name (string):name of file to create .txt
        
        Returns:
            None.
        """ 
        objFile = open(strFileName, 'a')
        objFile.close()
                   
    @staticmethod
    def save_entry(file_name, table):
        """Function to save current entries in memory to file
        
        Args:
            file_name (string): name of file to save data to
            table (list of dict): 2D data structure (list of dicts) that hold the data during runtime
            
        Returns:
            None.
        """
        if strYesNo == 'y':
            with open(file_name,'wb') as fileObj:
                pickle.dump(table, fileObj)
            print('Inventory saved to .dat file.')
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """
        print('Menu\n\n[l] Load Inventory from .txt file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] Delete CD from Inventory\n[s] Save Inventory to binary file\n[x] Exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def user_entry():
        """Gets user input for CD entry
        
        Args:
            None.
        
        Returns:
            None.
        """
        try:
            strID = int(input('Enter ID: ').strip())
        except ValueError as e:
            print('That\'s not a number!')
            print(e)
            pass
        else:
            strTitle = input('What is the CD\'s title? ').strip()
            stArtist = input('What is the Artist\'s name? ').strip()
            return strID, strTitle, stArtist


# 1. When program starts, 
FileProcessor.write_file(strFileName)
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('Type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('Reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('Canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        cd_id, cd_title, cd_artist = IO.user_entry()
        # 3.3.2 Add item to the table
        DataProcessor.add_user_data(cd_id, cd_title, cd_artist, lstTbl)
        # 3.3.3 Display modified inventory to user
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        try:
            intIDDel = int(input('Which ID would you like to delete? ').strip())
        except ValueError as e:
            print('\nThat\'s not a number.')
            print(e)
        # 3.5.2 search thru table and delete CD
        else:
            DataProcessor.delete_entry(intIDDel, lstTbl)
        # 3.5.3 Display modified inventory to user
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to binary file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        FileProcessor.save_entry(strBinaryName, lstTbl)
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')