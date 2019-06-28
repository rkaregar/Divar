function agreement() {
    if (document.getElementById("is_agreement").checked) {
        this.previous_price = document.getElementById("price").value;
        document.getElementById("price").value = -1;
        document.getElementById("price").readOnly = true;
    } else {
        document.getElementById("price").value = this.previous_price;
        document.getElementById("price").readOnly = false;
    }
}