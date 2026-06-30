const predictBtn = document.getElementById("predictBtn")
const outputBox = document.getElementById("outputBox")

const levelSelect = document.getElementById("level")

const buildingInput = document.getElementById("building")
const floorInput = document.getElementById("floor")
const departmentInput = document.getElementById("department")
const zoneInput = document.getElementById("zone")


// ==========================================
// LOAD BUILDINGS
// ==========================================

async function loadBuildings() {

    const response = await fetch(
        "http://127.0.0.1:8004/buildings"
    )

    const buildings = await response.json()

    buildingInput.innerHTML =
        '<option value="">Select Building</option>'

    buildings.forEach(building => {

        buildingInput.innerHTML += `
            <option value="${building}">
                ${building}
            </option>
        `

    })

}


// ==========================================
// LOAD FLOORS
// ==========================================

buildingInput.addEventListener("change", async () => {

    const building = buildingInput.value

    floorInput.innerHTML =
        '<option value="">Loading...</option>'

    const response = await fetch(
        `http://127.0.0.1:8004/floors?building=${building}`
    )

    const floors = await response.json()

    floorInput.innerHTML =
        '<option value="">Select Floor</option>'

    floors.forEach(floor => {

        floorInput.innerHTML += `
            <option value="${floor}">
                ${floor}
            </option>
        `

    })

})


// ==========================================
// LOAD DEPARTMENTS
// ==========================================

floorInput.addEventListener("change", async () => {

    const building = buildingInput.value
    const floor = floorInput.value

    departmentInput.innerHTML =
        '<option value="">Loading...</option>'

    const response = await fetch(
        `http://127.0.0.1:8004/departments?building=${building}&floor=${floor}`
    )

    const departments = await response.json()

    departmentInput.innerHTML =
        '<option value="">Select Department</option>'

    departments.forEach(department => {

        departmentInput.innerHTML += `
            <option value="${department}">
                ${department}
            </option>
        `

    })

})


// ==========================================
// LOAD ZONES
// ==========================================

departmentInput.addEventListener("change", async () => {

    const building = buildingInput.value
    const floor = floorInput.value
    const department = departmentInput.value

    zoneInput.innerHTML =
        '<option value="">Loading...</option>'

    const response = await fetch(
        `http://127.0.0.1:8004/zones?building=${building}&floor=${floor}&department=${department}`
    )

    const zones = await response.json()

    zoneInput.innerHTML =
        '<option value="">Select Zone</option>'

    zones.forEach(zone => {

        zoneInput.innerHTML += `
            <option value="${zone}">
                ${zone}
            </option>
        `

    })

})


// ==========================================
// SHOW / HIDE FILTERS BASED ON LEVEL
// ==========================================

function updateFilters() {

    const level = levelSelect.value

    // Hide everything first
    buildingInput.parentElement.style.display = "none"
    floorInput.parentElement.style.display = "none"
    departmentInput.parentElement.style.display = "none"
    zoneInput.parentElement.style.display = "none"


    if (level === "building") {

        buildingInput.parentElement.style.display = "flex"

    }

    else if (level === "floor") {

        buildingInput.parentElement.style.display = "flex"
        floorInput.parentElement.style.display = "flex"

    }

    else if (level === "department") {

        buildingInput.parentElement.style.display = "flex"
        floorInput.parentElement.style.display = "flex"
        departmentInput.parentElement.style.display = "flex"

    }

    else if (level === "zone") {

        buildingInput.parentElement.style.display = "flex"
        floorInput.parentElement.style.display = "flex"
        departmentInput.parentElement.style.display = "flex"
        zoneInput.parentElement.style.display = "flex"

    }

}

updateFilters()

levelSelect.addEventListener("change", updateFilters)


// ==========================================
// PREDICT
// ==========================================

predictBtn.addEventListener("click", async () => {

    try {

        outputBox.value = "Generating prediction..."

        const level = levelSelect.value

        let url = `http://127.0.0.1:8004/predict?level=${level}`


        // ----------------------------------
        // BUILD URL DYNAMICALLY
        // ----------------------------------

        if (level === "building") {

            url += `&building=${buildingInput.value}`

        }

        else if (level === "floor") {

            url += `&building=${buildingInput.value}`
            url += `&floor=${floorInput.value}`

        }

        else if (level === "department") {

            url += `&building=${buildingInput.value}`
            url += `&floor=${floorInput.value}`
            url += `&department=${departmentInput.value}`

        }

        else if (level === "zone") {

            url += `&building=${buildingInput.value}`
            url += `&floor=${floorInput.value}`
            url += `&department=${departmentInput.value}`
            url += `&zone=${zoneInput.value}`

        }


        const response = await fetch(url)

        const data = await response.json()

        outputBox.value = JSON.stringify(data, null, 4)

    }

    catch (error) {

        outputBox.value = `Error:\n${error.message}`

    }

})


// ==========================================
// INITIAL LOAD
// ==========================================

loadBuildings()
