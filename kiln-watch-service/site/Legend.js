function Legend(width, debug) {
    const DEBUG = debug | false;
    const WIDTH = width;
    const MARGINS = {
        top: 50,
        right: 50,
        bottom: 15,
        left: 80
    };
    const CONTENT_HEIGHT = 25;
    const CONTENT_MARGINS = {
        top: 10,
        right: 10,
        bottom: 10,
        left: 10
    };
    const LABELS = [
        "Line Style",
        "Temperature (°F)",
        "Rate of Change (Δ°F/Hr)",
        "Sensor Name"
    ];
//    const HEIGHT = 150;
    const HEIGHT = MARGINS.top + CONTENT_MARGINS.top + MARGINS.bottom + CONTENT_MARGINS.bottom + CONTENT_HEIGHT;

    const PREFIX = "l_";

    this.createChart = function() {

        // The graph image
        var svg = d3.create("svg")
            .attr("width", WIDTH)
            .attr("height", HEIGHT)
            .attr("viewBox", [0, 0, WIDTH, HEIGHT])
            .attr("style", "max-width: 100%; height: auto; height: intrinsic;");

        // Title
        svg.append('text')
            .attr('class', 'chart-title')
            .text("Latest")
            .attr('x', MARGINS.left + (WIDTH - MARGINS.left - MARGINS.right) / 2)
            .attr('y', MARGINS.top / 3)
            .attr('alignment-baseline', 'top')
            .attr("text-anchor", "middle");

        // Border around SVG, used for debugging mostly
        if (DEBUG) {
            var borderPath = svg.append("rect")
                .attr("x", 0)
                .attr("y", 0)
                .attr("height", HEIGHT)
                .attr("width", WIDTH)
                .style("stroke", 'green')
                .style("fill", "none")
                .style("stroke-width", 1);
        }

        // Legend boundary
        var legendFrame = svg.append("rect")
            .attr("id", `${PREFIX}frame`)
            .attr("x", MARGINS.left)
            .attr("y", MARGINS.top)
            .attr("height", HEIGHT - MARGINS.top - MARGINS.bottom)
            .attr("width", WIDTH - MARGINS.left - MARGINS.right)
            .style("stroke", 'black')
            .style("fill", "none")
            .style("stroke-width", 1);

        // Labels
        var column_width = Math.floor((WIDTH - MARGINS.left - MARGINS.right - CONTENT_MARGINS.left - CONTENT_MARGINS.right) / LABELS.length);
        LABELS.forEach(function(label) {
            var index = LABELS.indexOf(label);
            svg.append('text')
                .text(label)
                .attr('x', (MARGINS.left + CONTENT_MARGINS.left + index * column_width) + column_width / 2)
                .attr('y', MARGINS.top + CONTENT_MARGINS.top + CONTENT_HEIGHT / 2)
                .attr('alignment-baseline', 'bottom')
                .attr("text-anchor", "middle");
//                .style("font-weight", 'bold');
        });

        return svg;
    }

    this.updateChartData = function(svg, data) {

        // Order data by index
        data.sort((a, b) => a.index - b.index);

        // Remove all chart elemetns
//        svg.selectAll("*").remove();

        var column_width = Math.floor((WIDTH - MARGINS.left - MARGINS.right - CONTENT_MARGINS.left - CONTENT_MARGINS.right) / LABELS.length);

        // Remove any existing data
        data.forEach(function(sensor) {
            d3.select(`#${PREFIX}${sensor.name}`).remove();
        });

        // Resize the svg
        var width = WIDTH
        var height = MARGINS.top + CONTENT_MARGINS.top + MARGINS.bottom + CONTENT_MARGINS.bottom + data.length * CONTENT_HEIGHT + CONTENT_HEIGHT;
        svg
            .attr("height", height)
            .attr("viewBox", [0, 0, WIDTH, height]);
        d3.select(`#${PREFIX}frame`).attr("height", `${height - MARGINS.top - MARGINS.bottom}`);

        // Draw the lines.
        var line_number = 0;
        data.forEach(function(sensor) {
            var g = svg.append('g')
                .attr('id', `${PREFIX}${sensor.name}`);
            var col1 = MARGINS.left + CONTENT_MARGINS.left + column_width / 2;
            var col2 = col1 + column_width;
            var col3 = col2 + column_width;
            var col4 = col3 + column_width;
            var row = MARGINS.top + CONTENT_MARGINS.top + (line_number + 1) * CONTENT_HEIGHT + CONTENT_HEIGHT;
            g.append('path')
                .attr('d', `M ${col1 - column_width * 0.45} ${row - CONTENT_HEIGHT / 2} l ${column_width * .9} 0`)
                .style('fill', 'none')
                .style('stroke', STROKE[sensor.index % STROKE.length])
                .style('stroke-dasharray', DASH[sensor.index % DASH.length]);
            g.append('text')
                .text(`${sensor.reports[sensor.reports.length - 1].temp}`)
                .attr('x', col2)
                .attr('y', row)
                .attr('alignment-baseline', 'bottom')
                .attr("text-anchor", "middle");
            if (sensor.ramps.length > 0) {
                g.append('text')
                    .text(`${sensor.ramps[sensor.ramps.length - 1].rate}`)
                    .attr('x', col3)
                    .attr('y', row)
                    .attr('alignment-baseline', 'bottom')
                    .attr("text-anchor", "middle");
            }
            g.append('text')
                .text(`${sensor.name}`)
                .attr('x', col4)
                .attr('y', row)
                .attr('alignment-baseline', 'bottom')
                .attr("text-anchor", "middle");
            line_number = line_number + 1;
        });
    }

}