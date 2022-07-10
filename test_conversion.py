import subprocess
import filecmp

def test_conversion():
    process = subprocess.Popen(['python', 'rewex.py', './test_files/input.csv','-o','./test_files/test_output.csv'],
                     stdout=subprocess.PIPE, 
                     stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    #assert filecmp.cmp('./test_files/test_output.csv', './test_files/output.csv')