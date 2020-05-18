An app that receives calls, and 'does work' i.e. adds a variable timeout. The app measures the average time taken over the past 10 calls. 
For each successful call, the timeout increases by 10ms. 

If the avg time taken goes > 2 secs, then it starts rejecting calls until the avg time reduces. When a call is rejected, the timeout is reduced. 


-- log in --
python3 -m venv .

source bin/activate

pip install -r requirements.txt


-- log out --
deactivate
