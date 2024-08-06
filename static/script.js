// The script is for the web from submission page.
// It adds a 1 second delay after the form is submitted.
// A window is displays notifying the user of a successful
// transaction.
//


//@author (Maddie Hirschfeld)
//@version (May 25, 2024)


document.getElementById("transactionForm").onsubmit = function () {
  setTimeout(function () {
    alert("Successful transaction.");
    window.close();
  }, 1000);
  return true;
};