import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.dates as mdates
from datetime import datetime
from dateutil.relativedelta import relativedelta

from AccountReport import AccountReport

accounts = {
        "R011065664":   "DOE ECA",
        #"R011065663":   "Cornell L1TF",
        #"R011065652":   "ORNL Accelerator 2022",
        "R011065625":   "DOE Base",
        #"R011065677":   "ORNL Accelerator 2023",
        "E011060067":   "Start-up",
    }

fys = ["2023", "2024"]
for a in accounts:
    acct_example = a

totalsNames = [
    "totalSponsorBudget",
    "totalCurrentPeriodExpenditures",
    "totalCumulativeExpenditures",
    "totalEncumbrances",
    "totalManualFundsReservations",
    "totalUnderOverSpent",
]

y = {}

x_labels = []

for account in accounts:
    x_labels.clear()
    y[account] = {}
    for totalsName in totalsNames:
        y[account][totalsName] = []

    for fy in fys:
        for period in range(1,13):
            #print (fy,period)
            x_labels.append(f"{fy}-{period}")
            inputPDFFileName = f"LedgerPDFs/FY{fy}_Period{period :03d}_{account}.pdf"
            # print(inputPDFFileName)
            if os.path.isfile(inputPDFFileName):
                print(f"Found report for {account} FY{fy} Period{period} ++++++")
                report = AccountReport(inputPDFFileName)
            else:
                # print(f"Missing report for {account} FY{fy} Period{period}")
                for item in y[account]:
                    y[account][item].append(0)
                continue

            for item in y[account]:
                y[account][item].append( getattr(report,item) )

fig, ax = plt.subplots()

length = len(y[acct_example]["totalSponsorBudget"])
x = range(1,length+1)
colors = ["tab:blue","tab:orange", "tab:green", "tab:purple", "tab:red"]


x_dates = [datetime.strptime(date, "%Y-%m") - relativedelta(months=6) for date in x_labels]

leg_plots = []
for iaccount,account in enumerate(accounts):
    ax.plot(x_dates,y[account]["totalSponsorBudget"],":",label=f"{account} Total Sponsor Budget",c=colors[iaccount])
    ax.fill(x_dates,y[account]["totalCumulativeExpenditures"],c=colors[iaccount],alpha=0.3)
    ax.plot(x_dates,y[account]["totalCumulativeExpenditures"],"o-",label=f"{account} Total Cumulative Expenditures",c=colors[iaccount])
    ax.plot(x_dates,
        [sum(tmp) for tmp in zip(y[account]["totalEncumbrances"],y[account]["totalCumulativeExpenditures"])]
        ,"--",label=f"{account} Total Encumbrances+Exp",c=colors[iaccount])

ax.set(xlabel='Date', ylabel='Dollars', ylim=[0,800000])#,xlim=[1,12])
ax.grid()

# Format the x-axis to show dates properly
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b \'%y'))
plt.xticks(rotation=45)

ax.legend(loc="upper left", fontsize="x-small")
fig.savefig("Budgets.pdf")
# plt.show()

plt.cla()
for iaccount,account in enumerate(accounts):
    ax.fill_between(x,y[account]["totalUnderOverSpent"],color=colors[iaccount],alpha=0.3)
    ax.plot(x_dates,y[account]["totalUnderOverSpent"],"o-",label=f"{account} Total Projected Over/Under Spent",color=colors[iaccount])

# Format the x-axis to show dates properly
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b \'%y'))
plt.xticks(rotation=45)

ax.set(xlabel='Date', ylabel='Dollars', ylim=[-20000,200000])#,xlim=[1,10])
ax.grid()
ax.legend(loc="upper left")

fig.savefig("OverUnder.pdf")

