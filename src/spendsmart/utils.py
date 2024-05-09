import functools
import inspect


def errctx(ctx: str):
    """Add context to raised exceptions."""

    def decorator_errctx(func):
        @functools.wraps(func)
        def errctx_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                signature = inspect.signature(func)
                bound_args = signature.bind(*args, **kwargs)

                bound_args.apply_defaults()

                merged_ctx = ctx.format(**bound_args.arguments)

                try:
                    new_exception = (type(e))(f"{merged_ctx} {str(e)}").with_traceback(
                        e.__traceback__
                    )
                except:
                    raise e

                raise new_exception

        return errctx_wrapper

    return decorator_errctx
