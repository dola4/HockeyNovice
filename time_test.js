        
        function updateTotalTimeInAllPlayers() {
            const allPlayersTable = document.getElementById('allPlayers');
            for (let row of allPlayersTable.rows) {
                if (row.id && row.id.endsWith('-on-ice')) {
                    const playerId = row.id.replace('-on-ice', '');
                    const allPlayersRow = allPlayersTable.querySelector(`tr[id="${playerId}"]`);
                    if (allPlayersRow) {
                        const existingTimeCell = allPlayersRow.querySelector('.time_on_ice');
                        const newTimeCell = row.querySelector('.time_on_ice .statValue');
                        const totalTime = addTimes(existingTimeCell.textContent, newTimeCell.textContent);
                        existingTimeCell.textContent = totalTime;
                    }
                }
            }
        }


        // Variables globales pour le chronomètre
        let matchTimer = null;
        let matchStartTime = null;

        function startMatch() {
            matchStartTime = new Date();
            matchTimer = setInterval(updateTimeOnIce, 1000); // Mettre à jour chaque seconde
        }


        
        function addTimes(time1, time2) {
            const splitTime1 = time1.split(':').map(Number);
            const splitTime2 = time2.split(':').map(Number);

            let hours = splitTime1[0] + splitTime2[0];
            let minutes = splitTime1[1] + splitTime2[1];
            let seconds = splitTime1[2] + splitTime2[2];

            // Gérer les débordements de minutes et secondes
            minutes += Math.floor(seconds / 60);
            seconds %= 60;
            hours += Math.floor(minutes / 60);
            minutes %= 60;

            // Formater en hh:mm:ss
            return [hours, minutes, seconds].map(v => String(v).padStart(2, '0')).join(':');
        }


        function updateAllPlayersTimeOnIce() {
            updateTimeOnIceForTable(document.getElementById('playersOnIce'));
            updateTimeOnIceForTable(document.getElementById('goalerOnIce'));
        }
        function updateTimeOnIceForTable(table) {
            for (let row of table.rows) {
                if (row.id) {
                    updateTimeOnIceForPlayer(row.id);
                }
            }
        }

        function updateTimeOnIce() {
            console.log("Mise à jour du temps sur la glace");
            const currentTime = new Date();
            const elapsedSeconds = Math.floor((currentTime - matchStartTime) / 1000);
            // Mettre à jour le temps sur la glace pour chaque joueur sur la glace
            updateAllPlayersTimeOnIce();
        }

        function updateTimeOnIceForPlayer(playerId) {
            const playerRow = document.getElementById(playerId);
            console.log("Mise à jour du temps pour le joueur:", playerId);
            if (playerRow) {
                const timeOnIceCell = playerRow.querySelector('.time_on_ice .statValue');
                if (!timeOnIceCell) {
                    console.error("Élément Time On Ice non trouvé pour le joueur:", playerId);
                    return;
                }
                let currentTimeOnIce = timeOnIceCell.textContent;
                // Conversion de currentTimeOnIce en secondes
                let timeParts = currentTimeOnIce.split(':').map(part => parseInt(part, 10));
                let totalSeconds = timeParts[0] * 3600 + timeParts[1] * 60 + timeParts[2];
                totalSeconds += 1; // Incrémenter de 1 seconde
        
                // Reconvertissez en format hh:mm:ss
                let hours = Math.floor(totalSeconds / 3600);
                let minutes = Math.floor((totalSeconds % 3600) / 60);
                let seconds = totalSeconds % 60;
        
                // Formatage pour maintenir deux chiffres
                let formattedTime = [hours, minutes, seconds].map(part => part.toString().padStart(2, '0')).join(':');
                timeOnIceCell.textContent = formattedTime;
            }
        }
        