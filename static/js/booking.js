// Calculate total price for movie booking
document.addEventListener('DOMContentLoaded', function() {
    const seatsInput = document.querySelector('input[name="number_of_seats"]');
    const totalPriceSpan = document.getElementById('totalPrice');
    const pricePerTicketElement = document.getElementById('pricePerTicket');
    
    if (seatsInput && totalPriceSpan && pricePerTicketElement) {
        const pricePerTicket = parseFloat(pricePerTicketElement.dataset.price);
        
        seatsInput.addEventListener('input', function() {
            const seats = parseInt(this.value) || 1;
            const total = (seats * pricePerTicket).toFixed(2);
            totalPriceSpan.textContent = total;
        });
    }
});
