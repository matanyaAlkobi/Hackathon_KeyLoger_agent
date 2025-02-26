function get_input(){
    let name_in = document.getElementById("name").value;
    console.log(name_in)
}
    
function validateForm(){
    let name = document.getElementById('name').value;
    let password = document.getElementById('password').value;
    if (name === "" || password === ""){
        document.getElementById('messege').textContent = 'you must full all ';
        return false;
    }
    return true;


}
