from cx_Freeze import setup, Executable

setup(
    name='Game of life',
    version='0.1',
    description='Implement the game of life with a list of pattern available',
    executables=[Executable('main.py')]
)
