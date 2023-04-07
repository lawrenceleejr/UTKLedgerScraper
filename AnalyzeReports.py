import matplotlib.pyplot as plt
import numpy as np
import os

from AccountReport import AccountReport

accounts = [
    "R011065670",
    "R011065645"
]

fys = ["2023"]

totalsNames = [
    "totalSponsorBudget",
    "totalCurrentPeriodExpenditures",
    "totalCumulativeExpenditures",
    "totalEncumbrances",
    "totalManualFundsReservations",
    "totalUnderOverSpent",
]

y = {}

for account in accounts:
    y[account] = {}
    for totalsName in totalsNames:
        y[account][totalsName] = []

    for fy in fys:
        for period in range(1,13):
            # print (fy,period)
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

length = len(y["R011065670"]["totalSponsorBudget"])
x = range(1,length+1)
colors = ["tab:blue","tab:orange"]

for iaccount,account in enumerate(accounts):
    ax.plot(x,y[account]["totalSponsorBudget"],":",label=f"{account} Total Sponsor Budget",c=colors[iaccount])
    ax.fill(x,y[account]["totalCumulativeExpenditures"],c=colors[iaccount],alpha=0.3)
    ax.plot(x,y[account]["totalCumulativeExpenditures"],"o-",label=f"{account} Total Cumulative Expenditures",c=colors[iaccount])
    ax.plot(x,
        [sum(tmp) for tmp in zip(y[account]["totalEncumbrances"],y[account]["totalCumulativeExpenditures"])]
        ,"--",label=f"{account} Total Encumbrances+Exp",c=colors[iaccount])

ax.set(xlabel='Period in FY2023', ylabel='Dollars', ylim=[0,200000],xlim=[1,9])
ax.grid()
ax.legend(loc="upper left")

fig.savefig("Budgets.pdf")
# plt.show()

plt.cla()
for iaccount,account in enumerate(accounts):
    ax.fill_between(x,y[account]["totalUnderOverSpent"],color=colors[iaccount],alpha=0.3)
    ax.plot(x,y[account]["totalUnderOverSpent"],"o-",label=f"{account} Total Projected Over/Under Spent",color=colors[iaccount])

ax.set(xlabel='Period in FY2023', ylabel='Dollars', ylim=[-100,50000],xlim=[1,9])
ax.grid()
ax.legend(loc="upper left")

fig.savefig("OverUnder.pdf")

