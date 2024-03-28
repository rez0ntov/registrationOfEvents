function toggleButton()
            {
                var eventname = document.getElementById('eventname').value;
                var date1 = document.getElementById('date1').value;
                var date2 = document.getElementById('date2').value;
                var team = document.getElementById('team').value;
 
 
                if (eventname || date1 || date2 || team) {
                    document.getElementById('submitButton').disabled = false;
                } else {
                    document.getElementById('submitButton').disabled = true;
                }
            }