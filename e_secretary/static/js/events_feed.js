// function generate_events_pages(displayRecords) {
//   var html;
//   var dateRuler;
//   var dateColorClass;
//   $('#events').html('');

//   for (var i = 0; i < displayRecords.length; i++) {
//     var datep = displayRecords[i].event_date;

//     if ((Date.parse(datep) - Date.parse(new Date())) > 0) {
//       dateRuler = "bg-primary"
//       dateColorClass = "text-primary"
//     } else {
//       dateRuler = "date-bg-secondary"
//       dateColorClass = "date-text-secondary"
//     }

//     html = `
//       <div class="col-xl-4 col-lg-6 col-xs-12">
//         <div class="events_page my-3">
//           <div class="events_title pt-3 ml-4">
//             <strong> ${displayRecords[i].event_title} </strong>
//           </div>
//           <hr class="events_ruler">
//           <div>
//             <p class="events_info ml-4">
//               <span class="events_date ${dateColorClass}">${displayRecords[i].event_date}</span>
//               <span class="events_location">@ ${displayRecords[i].event_location}</span>
//             </p>
//           </div>
//           <br>
//           <hr class="events_date_ruler ${dateRuler}">
//         </div>
//       </div>
//      `
//     $('#events').append(html);
//   }
// }

// function apply_pagination(records, $pagination, displayRecords, totalPages, recPerPage) {
//   if (records.length < 1) {
//     $('#events_container').hide();
//   } else {
//     $('#events_container').show();
//     $pagination.twbsPagination({
//       totalPages: totalPages,
//       visiblePages: 6,
//       loop: true,
//       next: '>',
//       prev: '<',
//       hideOnlyOnePage: true,
//       onPageClick: function (event, page) {
//         displayRecordsIndex = Math.min(page - 1, 1) * recPerPage;
//         endRec = (displayRecordsIndex) + recPerPage;
//         displayRecords = records.slice(displayRecordsIndex, endRec);
//         generate_events_pages(displayRecords);
//       }
//     });
//   }
// }

// function generate_events() {

//   $.getScript('static/js/twbs-pagination/jquery.twbsPagination.js', function () {

//     $('#events_container').hide();

//     var $pagination = $('#events_pagination'),
//       totalRecords = 0,
//       records = [],
//       displayRecords = [],
//       recPerPage = 3,
//       page = 1,
//       totalPages = 0;

//     $.ajax({
//       url: "https://api.myjson.com/bins/9ze5y",
//       async: true,
//       dataType: 'json',
//       success: function (data) {
//         records = data;
//         totalRecords = records.length;
//         totalPages = Math.ceil(totalRecords / recPerPage);
//         apply_pagination(records, $pagination, displayRecords, totalPages, recPerPage);
//       }
//     });
//   });
// };

// //// Function to change pagination items count on each page
// // $(window).on('resize', function(){
// //   var win = $(this); //this = window
// //   if (win.height() >= 820) {

// //    }
// //   if (win.width() >= 1280) {

// //    }
// // });
