function toggleButton()
            {
                var tname = document.getElementById('tname').value;
                var pname = document.getElementById('pname').value;
                var name2 = document.getElementById('name2').value;
                var name3 = document.getElementById('name3').value;
                var email4 = document.getElementById('email4').value;
 
 
                if (tname && pname && name2 && name3 && email4) {
                    document.getElementById('submitButton').disabled = false;
                } else {
                    document.getElementById('submitButton').disabled = true;
                }
            }