from pytest import mark
from honeybadgermpc.betterpairing import G1, ZR
from honeybadgermpc.secretshare_hbavsslight import HbAvssDealer, HbAvssRecipient
from honeybadgermpc.router import simple_router
import asyncio


@mark.asyncio
async def test_hbavss():
    # TODO: We need to generate the CRS once and hardcode it as a parameter
    crs = [G1.rand(), G1.rand()]
    t = 2
    n = 3*t + 1
    participantids = list(range(0, n))
    dealerid = n
    sid = 1
    (participantpubkeys, participantprivkeys) = ({}, {})
    for i in participantids:
        sk = ZR.rand()
        participantprivkeys[i] = sk
        participantpubkeys[i] = crs[0] ** sk
    pubparams = (t, n, crs, participantids, participantpubkeys, dealerid, sid)

    sends, recvs = simple_router(len(participantids) + 1)
    dealer = HbAvssDealer(pubparams, (42, dealerid), sends[dealerid], recvs[dealerid])
    threads = []
    recipients = []
    for i in participantids:
        recipients.append(HbAvssRecipient(pubparams, (i, participantprivkeys[i]),
                                          sends[i], recvs[i]))
    for r in recipients:
        threads.append(r.run())
    threads.append(dealer.run())
    await asyncio.wait(threads)