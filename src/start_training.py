from learning.tasks import celery_aggregate


def main():
    res = celery_aggregate.apply_async(
        kwargs={"list_local_models": {}, "global_epoch": 0},
        queue="aggregator",
        countdown=1,
    )
    print(res.state)
    res.get(propagate=False)
    print(res.successful())
    print(res.state)


if __name__ == "__main__":
    main()
