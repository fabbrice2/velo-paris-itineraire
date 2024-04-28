let moreEditDel = document.querySelectorAll(".more-edit-del");
let moreBtn = document.querySelectorAll(".button-more");
let moreEditDelClose = document.querySelectorAll(
  ".more-edit-del .more-edit-del-close"
);

function openMoreEditDel(event) {
  moreEditDel.forEach(function (item) {
    item.style.display = "block";
  });

  moreBtn.forEach(function (item) {
    item.style.display = "none";
  });
}

function closeMoreEditDel() {
  moreEditDel.forEach(function (item) {
    item.style.display = "none";
  });

  moreBtn.forEach(function (item) {
    item.style.display = "block";
  });
}

moreBtn.forEach(function (item) {
  item.addEventListener("click", openMoreEditDel);
});

moreEditDelClose.forEach(function (item) {
  item.addEventListener("click", closeMoreEditDel);
});

let editBtnChange = document.querySelectorAll(".edit-btn-change");
let editBtn = document.querySelectorAll(".edit-btn");
let locationInput = document.querySelectorAll(".location");
let cancelBtn = document.querySelectorAll(".cancel-btn");

function hideAll() {
  for (let i = 0; i < editBtnChange.length; i++) {
    editBtnChange[i].style.display = "none";
    locationInput[i].style.display = "none";
    cancelBtn[i].style.display = "none";
  }
}

for (let i = 0; i < editBtn.length; i++) {
  editBtn[i].addEventListener("click", function () {
    hideAll();

    editBtnChange[i].style.display = "block";
    locationInput[i].style.display = "block";

    cancelBtn[i].style.display = "block";

    editBtn[i].style.display = "none";

    for (let j = 0; j < editBtn.length; j++) {
      if (j !== i) {
        editBtn[j].disabled = true;
      }
    }
  });
}

for (let i = 0; i < editBtnChange.length; i++) {
  editBtnChange[i].addEventListener("click", function () {
    editBtn[i].style.display = "inline-block";

    hideAll();

    for (let j = 0; j < editBtn.length; j++) {
      editBtn[j].disabled = false;
    }
  });
}

for (let i = 0; i < cancelBtn.length; i++) {
  cancelBtn[i].addEventListener("click", function () {
    editBtn[i].style.display = "inline-block";

    hideAll();

    for (let j = 0; j < editBtn.length; j++) {
      editBtn[j].disabled = false;
    }
  });
}
