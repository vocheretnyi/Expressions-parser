let ctx;

$(document).ready(() => {
    ctx = document.getElementById('plot-canvas').getContext('2d');
    Chart.defaults.line.spanGaps = true;
    $('#submit-btn').click(calculate);
})

function calculate() {
    let form = {
        f: $('#function-input').val(),
        x: parseFloat($('#var-value').val()),
        tab: {
            from: parseFloat($('#tab-from').val()),
            to: parseFloat($('#tab-to').val()),
            step: parseFloat($('#tab-step').val()),
        }
    }
    $.post('/calc', {data: JSON.stringify(form)})
        .done(res => {
            $('#result-output').text(res.result.toFixed(5));
            $('#tokens').empty();
            $('#tokens').append(res.tokens);
            $('#errors').empty();
            let tab = res.tab.map(item => {
                return {x: item[0], y: item[1]}
            });
            let labels = res.tab.map(item => item[0]);
            new Chart(ctx, {
                type: 'line', data: {
                    labels: labels,
                    datasets: [{
                        label: 'f',
                        backgroundColor: 'rgb(255, 204, 204)',
                        borderColor: 'rgb(255, 99, 132)',
                        data: tab
                    }]
                }
            });
            $('.result-block').css('visibility', 'visible');
        })
        .fail(err => {
            $('#errors').empty();
            $('#errors').append(err.responseText);
        })
}