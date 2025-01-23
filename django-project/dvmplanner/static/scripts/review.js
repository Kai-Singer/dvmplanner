const timeToSeconds = (time) => {
  const [hours, minutes, seconds] = time.split(':').map(x => Number(x));
  return hours * 3600 + minutes * 60 + seconds;
};

const secondsToHMS = (seconds) => {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = seconds % 60;
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
};

const modules = reviewData.map(data => data.module);
const timeData = reviewData.map(data => timeToSeconds(data.time));
const sessionsData = reviewData.map(data => data.sessions);

const timeChart = document.getElementById('review_chart_time');

new Chart(timeChart, {
  type: 'pie',
  data: {
    labels: modules,
    datasets: [{
      data: timeData
    }]
  },
  options: {
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const total = context.dataset.data.reduce((a, b) => a + b, 0);
            const percentage = ((context.raw / total) * 100).toFixed(2).replace('.', ',');
            const formattedTime = secondsToHMS(context.raw);
            return ` ${formattedTime} (${percentage}%)`;
          }
        }
      }
    }
  }
});

const sessionsChart = document.getElementById('review_chart_sessions');

new Chart(sessionsChart, {
  type: 'pie',
  data: {
    labels: modules,
    datasets: [{
      data: sessionsData
    }]
  },
  options: {
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            return ` ${context.raw} Sitzungen`;
          }
        }
      }
    }
  }
});

function downloadPdf(uid) {
  //
}