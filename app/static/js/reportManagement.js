document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.delete-report').forEach(button => {
        button.addEventListener('click', function() {
            const reportId = this.dataset.reportId;
            fetch(`/report/delete/${reportId}`, { method: 'DELETE' })
                .then(response => response.json())
                .then(data => {
                    if(data.success) {
                        alert('Report successfully deleted.');
                        window.location.reload();  // Reload the page to reflect the deletion
                    } else {
                        alert('Failed to delete the report.');
                    }
                });
        });
    });
});


$(document).ready(function(){
    $("#searchInput").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#reportTable tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });

  function sortTable() {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("tableSorting");
    switching = true;

    while (switching) {
        switching = false;
        rows = table.rows;

        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("td")[0]; // Change the index to target the second column (First Name)
            y = rows[i + 1].getElementsByTagName("td")[0]; // Change the index to target the second column (First Name)

            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                shouldSwitch = true;
                break;
            }
        }

        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
}