function toggleButton()
            {
                var pname = document.getElementById('pname').value;
                var name2 = document.getElementById('name2').value;
                var name3 = document.getElementById('name3').value;
 
                if (pname && name2 && name3) {
                    document.getElementById('submitButton').disabled = false;
                } else {
                    document.getElementById('submitButton').disabled = true;
                }
            }