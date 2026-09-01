console.log("SCRIPT LOADED");


// ===============================
// IMAGE PREVIEW
// ===============================

const imageInput = document.getElementById("image");
const preview = document.getElementById("preview");


imageInput.addEventListener("change", function(){

    const file = this.files[0];


    if(file){

        const reader = new FileReader();


        reader.onload = function(e){

            preview.src = e.target.result;

        };


        reader.readAsDataURL(file);

    }

});





// ===============================
// BUTTON EVENT
// ===============================


document
.getElementById("predictBtn")
.onclick = function(){

    console.log("BUTTON CLICKED");

    predict();

    return false;

};






// ===============================
// PREDICTION FUNCTION
// ===============================


async function predict(){

alert("predict started");
    console.log("PREDICT START");



    const imageFile =
    document
    .getElementById("image")
    .files[0];



    if(!imageFile){


        alert(
            "Please select satellite image"
        );


        return;

    }




    const result =
    document.getElementById("result");



    result.innerHTML = `

    <h2>
    ⏳ Analyzing...
    </h2>

    <p>
    AI models are processing image and climate data
    </p>

    `;





    let formData = new FormData();



    formData.append(
        "image",
        imageFile
    );





    let features = [


        "MonsoonIntensity",
        "TopographyDrainage",
        "RiverManagement",
        "Deforestation",
        "Urbanization",
        "ClimateChange",
        "DamsQuality",
        "Siltation",
        "AgriculturalPractices",
        "Encroachments",
        "IneffectiveDisasterPreparedness",
        "DrainageSystems",
        "CoastalVulnerability",
        "Landslides",
        "Watersheds",
        "DeterioratingInfrastructure",
        "PopulationScore",
        "WetlandLoss",
        "InadequatePlanning",
        "PoliticalFactors"


    ];






    features.forEach(function(feature){


        let input =
        document.getElementById(feature);



        if(input){


            formData.append(
                feature,
                input.value
            );


        }


    });







    try{


        console.log("SENDING REQUEST");



        const response =
        await fetch(

            "http://127.0.0.1:5000/final_prediction",

            {

                method:"POST",

                body:formData

            }

        );





        console.log(
            "STATUS:",
            response.status
        );





        const data =
        await response.json();




        console.log(
            "JSON RECEIVED"
        );


        console.log(data);






        let color="green";


        if(data.warning.includes("HIGH")){

            color="red";

        }

        else if(data.warning.includes("MEDIUM")){

            color="orange";

        }







        result.innerHTML = `



        <h2 style="color:${color}">

        🚨 ${data.warning}

        </h2>



        <hr>



        <h3>
        🛰 Satellite Image Analysis
        </h3>


        <p>

        Flood Probability:

        <b>
        ${(data.image_probability*100).toFixed(2)}%
        </b>

        </p>





        <h3>
        🌦 Climate Analysis
        </h3>


        <p>

        Climate Risk:

        <b>
        ${(data.climate_risk*100).toFixed(2)}%
        </b>

        </p>







        <h3>
        🤖 Final AI Decision
        </h3>


        <p>

        Final Risk Score:

        <b>
        ${(data.final_score*100).toFixed(2)}%
        </b>

        </p>


        `;




    }




    catch(error){


        console.log(
            "ERROR:",
            error
        );



        result.innerHTML = `


        <h2 style="color:red">

        ❌ Prediction Failed

        </h2>


        <p>

        ${error.message}

        </p>


        `;


    }


}