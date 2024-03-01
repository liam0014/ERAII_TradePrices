# ERAII_TradePrices
An automated trade price analyser for the Buccaneers Reef Historical ERAS II mod for their own Maelstrom engine

## Instructions
I recommend running the Python script file directly, if you can/know how to.
This way you can edit the CSV file path to a fixed value for your game, saving the hassle of manually entering the file path and file name.
Additionally, you can edit the weight values if you don't use ERAS' "realistic" weight setting.

If you are unable to run the Python script directly, there is a Windows EXE file that was produced using PyInstaller.
You can just download and execute this as any normal program, no installation required.

### Use guide
On running the script or launching the application you'll be asked to enter in the folder path of your ERAS II game files and the file name of you TradePrices {gameName}.CSV.
The value you enter in this prompt should be something like: C:\Games\gentlemen-of-fortune-historical-eras-module-2\TradePrices Player.csv
There is no need to place apostrophes, quotation marks or any other wrapper around this file path.

Note: there is error checking to ensure this is a CSV but no checking to ensure it is the right CSV.

After entering a valid file path you will be presented with a menu

```
Select an option:
1. Find the best trade
2. Select origin and destination ports
3. Refresh CSV data
4. Exit
```

Options 1 and 2 will both first ask you for your departure port, select a number from the list for whichever port this is.
Option 1 will then compare all the prices with this port and give you a single best trade route, based on profit per weight.
Option 2 will ask for your destination port, select this and then you will get a printout of every available trade and their profit/loss. This list is order via profit per weight descending.
Option 3 will just reload the same CSV file that you selected, so if you are playing the game and make a new CSV file after you've been to more ports, use this option the data held in the program.

On exit all data in the program will be lost, your trade data won't be saved for the next time.
