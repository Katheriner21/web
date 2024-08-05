const createOrder = async () => {
    try {
      const response = await fetch("/api/orders", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          cart: [
            {
              id: "123",
              quantity: "1",
            },
          ],
        }),
      });
  
      const orderData = await response.json();

      console.log(orderData.json_response.id);
  
      if (orderData.json_response.id) {
        console.log(orderData.json_response.id)
        return orderData.json_response.id;
      } else {
        throw new Error(JSON.stringify(orderData));
      }
    } catch (error) {
      console.error(error);
      resultMessage(`No se pudo iniciar el pago de PayPal...<br><br>${error}`);
    }
  };
  
  const onApprove = async (data, actions) => {
    try {
      const response = await fetch(`/api/orders/${data.orderID}/capture`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
  
      const orderDatas = await response.json();
      const orderData = orderDatas.json_response
      console.log(orderData);
  
      const errorDetail = orderData?.details?.[0];
  
      if (errorDetail?.issue === "INSTRUMENT_DECLINED") {
        return actions.restart();
      } else if (errorDetail) {
        throw new Error(`${errorDetail.description} (${orderData.debug_id})`);
      } else if (!orderData.purchase_units) {
        throw new Error(JSON.stringify(orderData));
      } else {
        const transaction =
          orderData?.purchase_units?.[0]?.payments?.captures?.[0] ||
          orderData?.purchase_units?.[0]?.payments?.authorizations?.[0];
        resultMessage(
          `Transaction ${transaction.status}: ${transaction.id}<br><br>See console for all available details`,
        );
        console.log(
          "Capture result",
          orderData,
          JSON.stringify(orderData, null, 2),
        );
        /*fetch("/agg_sub/"+user+"/")
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    // Recargar la página después de que se complete la solicitud AJAX
                    window.location.href = "/Perfilcontenido/"+user;
                })
                .catch(error => {
                    console.error('Fetch error:', error);
                });*/
      }
    } catch (error) {
      console.error(error);
      resultMessage(
        `Lo sentimos, su transacción no pudo ser procesada...<br><br>${error}`,
      );
    }
  };
  
  window.paypal
    .Buttons({
      style: {
        shape: "pill",
        layout: "vertical",
      },
      createOrder: createOrder,
      onApprove: onApprove,
    })
    .render("#paypal-button-container");
  
  function resultMessage(message) {
    const container = document.querySelector("#result-message");
    container.innerHTML = message;
  }
  