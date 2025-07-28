
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('select').forEach(select => {
    select.addEventListener('focus', () => {
      select.style.borderColor = '#2980b9';
    });
    select.addEventListener('blur', () => {
      select.style.borderColor = '#ccc';
    });
  });
});

// Clone and add new time slot
  function addTimeSlot() {
    const container = document.getElementById('time-slots-container');
    const firstSlot = container.querySelector('.time-slot');
    const newSlot = firstSlot.cloneNode(true);

    // Reset all selects to default
    newSlot.querySelectorAll('select').forEach(select => select.selectedIndex = 0);

    // Add event listener to new remove button
    newSlot.querySelector('.remove-btn').addEventListener('click', function () {
      removeSlot(this);
    });

    container.appendChild(newSlot);
  }

  // Remove a time slot
  function removeSlot(button) {
    const container = document.getElementById('time-slots-container');
    if (container.querySelectorAll('.time-slot').length > 1) {
      button.closest('.time-slot').remove();
    }
  }

  // Ensure existing Remove buttons work on page load
  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('.remove-btn').forEach(btn => {
      btn.addEventListener('click', () => removeSlot(btn));
    });
  });

let totalClassrooms = 0;
let currentIndex = 0;
let classroomData = [];

function prepareSingleClassroomEntry() {
  totalClassrooms = parseInt(document.getElementById("num_classrooms").value);
  classroomData = Array.from({ length: totalClassrooms }, (_, i) => ({
    name: `Classroom ${i + 1}`,
    seating: [80, 85, 90][i % 3],
    ownership: "Owned",
    students: ""
  }));

  let rentedIndexes = [];
  while (rentedIndexes.length < Math.min(5, totalClassrooms)) {
    let idx = Math.floor(Math.random() * totalClassrooms);
    if (!rentedIndexes.includes(idx)) rentedIndexes.push(idx);
  }
  for (let idx of rentedIndexes) {
    classroomData[idx].ownership = "Rented";
  }

  currentIndex = 0;
  renderClassroomInput();
}

function renderClassroomInput() {
  const c = classroomData[currentIndex];
  document.getElementById("single-classroom-entry").innerHTML = `
    <h3>${c.name}</h3>
    <p><strong>Seating Capacity:</strong> ${c.seating}</p>
    <p><strong>Ownership:</strong> ${c.ownership}</p>
    <label><strong>Allotted Students:</strong></label>
    <input type="number" name="students[]" min="0" value="${c.students}" required>
    <input type="hidden" name="classroom_names[]" value="${c.name}">
    <input type="hidden" name="seating_capacities[]" value="${c.seating}">
    <input type="hidden" name="ownerships[]" value="${c.ownership}">
    <p><em>Classroom ${currentIndex + 1} of ${totalClassrooms}</em></p>
  `;
}

function nextClassroom() {
  const studentInput = document.querySelector('input[name="students[]"]');
  if (studentInput) {
    classroomData[currentIndex].students = studentInput.value;
  }
  if (currentIndex < totalClassrooms - 1) {
    currentIndex++;
    renderClassroomInput();
  }
}

function prevClassroom() {
  const studentInput = document.querySelector('input[name="students[]"]');
  if (studentInput) {
    classroomData[currentIndex].students = studentInput.value;
  }
  if (currentIndex > 0) {
    currentIndex--;
    renderClassroomInput();
  }
}

    // facultyData will be injected from Jinja template
let facultyData = {};
