/*
 * multiline.js
 * Generic multiline chart functionality wrapping D3
 *
 * Author:  Benjamin Bengfort <benjamin@bengfort.com>
 * Created: Thu Jun 04 09:10:41 2015 -0400
 */

(function() {

  MultilineChart = function(selector, options) {

    this.svg     = null;
    this.elem    = null;
    this.margins = {
      top: 10,
      right: 10,
      bottom: 36,
      left: 24
    }

    this.colors  = d3.scale.category10();
    this.lines   = {};
    this.hidden  = {};

    /*
     * Initializes the MultilineChart in a div with various options.
     */
    this.init = function(selector, options) {
      this.elem = $(selector);

      if (options) {
        if (options.margins) {
          this.margins = _.defaults(options.margins, this.margins);
        }
      }

      this.draw();
      console.log("MultilineChart on " + selector + " initialized!");

      return this;
    }

    /*
     * Add data to the multiline chart. The label should be the name of the
     * series/line to add. Data should be an array of objects as follows:
     *   data = {
     *      date: new Date(),
     *     count: 10
     *   }
     */
    this.add_line = function(label, data) {
      var self = this;
      _.each(data, function(d) {
        d.date = self.parse_date(d.date);
      });

      // Add the data to the class
      this.hidden[label] = false;
      this.lines[label]  = data;

      // Map color domain to lines
      this.colors = this.colors.domain(self.lines);

      // Re-render the graph
      this.draw();
    }

    this.hide_line = function(label) {
      // Hides a line already added to chart
      if (!this.hidden[label]) {
        this.hidden[label] = true;
        this.draw();
      }

    }

    this.show_line = function(label) {
      // Shows a line that has been hidden
      if (this.hidden[label]) {
        this.hidden[label] = false;
        this.draw();
      }
    }

    this.draw = function() {
      var self = this;
      var all_data = _.flatten(
        _.values(
          _.pick(self.lines, function(val, key, obj) { return !self.hidden[key] })
        )
      );

      // Clear out the old svg
      if (this.svg) {
        this.svg.remove();
      }

      // Create the new svg
      this.svg = d3.select(selector).append("svg")
          .attr("width", this.width())
          .attr("height", this.height());

      // Domain of xScale needs to be inferred from data
      var xScale = d3.time.scale()
        .range([0, this.width(true)])
        .domain([
          d3.min(all_data, function(d) { return d.date }),
          d3.max(all_data, function(d) { return d.date })
        ]);

      // Domain of yScale needs to be inferred from data
      var yScale = d3.scale.linear()
        .range([this.height(true), 0])
        .domain([
          d3.min(all_data, function(d) { return d.count }),
          d3.max(all_data, function(d) { return d.count })
        ]);

      // Function that renders the line with the x and y scale.
      var linef = d3.svg.line()
        .interpolate('basis')
        .x(function(d) { return xScale(d.date); })
        .y(function(d) { return yScale(d.count); });

      var interval = d3.time.day;

      // Create Axes
      xAxis = d3.svg.axis()
        .scale(xScale)
        .orient("bottom")
        .ticks(7)
        .tickFormat(d3.time.format('%b %_d'));

      yAxis = d3.svg.axis()
        .scale(yScale)
        .tickFormat(d3.format("s"))
        .orient("left");

      // Append the xAxis to the svg
      this.svg.append("svg:g")
          .attr("class","axis")
          .attr("transform", this.translate("bottom"))
        .call(xAxis)
        .selectAll("text")
          .attr("transform", function(d) {
              return "rotate(25)translate(" + this.getBBox().width/2 + "," +
            this.getBBox().height/2 + ")";
          });

      // Append the yAxis to the svg
      this.svg.append("svg:g")
          .attr("class","axis")
          .attr("transform", this.translate("left"))
        .call(yAxis)
        .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".71em")
          .style("text-anchor", "end")
          .text("topics");

      // Add lines to the graph
      _.each(self.lines, function(data, name) {

        if (self.hidden[name]) {
          return;
        }

        var g = self.svg.append("svg:g");

        g.append("path")
          .datum(data)
          .attr("class", "line")
          .attr("d", linef)
          .attr("transform", self.translate("left"))
          .style("stroke", self.colors(name));

      });
    }


    // Helper functions to get the width from the element
    // If the inner argument is true, the margins are subtracted
    this.width = function(inner) {
      if (inner) {
        return this.elem.width() - this.margins.left - this.margins.right;
      } else {
        return this.elem.width();
      }

    }

    // Helper functions to get the height from the element
    // If the inner argument is true, the margins are subtracted
    this.height = function(inner) {
      if (inner) {
        return this.elem.height() - this.margins.top - this.margins.bottom;
      } else {
        return this.elem.height();
      }

    }

    // Helper function to determine translation properties
    this.translate = function(position) {
      var align = [0, 0];

      if (position == 'left') {
        align[0] = this.margins.left;
        align[1] = this.margins.top;
      } else if (position == 'bottom') {
        align[0] = this.margins.left;
        align[1] = this.height() - this.margins.bottom;
      }

      return "translate(" + align[0] + "," + align[1] + ")";

    }

    // Helper function to parse date strings
    this.dateFormat = d3.time.format("%Y-%m-%d");
    this.parse_date = function(d) {
      return this.dateFormat.parse(d);
    }


    return this.init(selector, options);
  }

})();
