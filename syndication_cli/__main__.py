import typer

from syndication_cli.adder import add
from syndication_cli.collector import collect
from syndication_cli.config import load_config, setup_logging
from syndication_cli.corrector import correct
from syndication_cli.models import SyndicationConfig
from syndication_cli.replay import replay
from syndication_cli.tagger import tagger

DEFAULT_CONFIG_PATH = "config/syndication.yaml"
DEFAULT_DRY_RUN = False
DEFAULT_VERBOSE = False

app = typer.Typer(help="Syndication CLI - Manage cross-posting from social media to your blog")


def get_config(
    config_path: str,
    dry_run: bool,
    verbose: bool,
    config: SyndicationConfig | None = None,
) -> SyndicationConfig:
    """
    Carica la configurazione e applica i flag dry_run e verbose.

    Args:
        config_path: Percorso al file di configurazione YAML.
        dry_run: Se True, esegue in modalita' simulazione senza modificare dati.
        verbose: Se True, abilita output dettagliato.
        config: Oggetto configurazione gia' caricato (opzionale).

    Returns:
        Oggetto SyndicationConfig con le opzioni aggiornate.
    """
    if config is None:
        config = load_config(config_path)

    if dry_run:
        config.options.dry_run = True
    if verbose:
        config.options.verbose = True

    setup_logging(config.options.verbose)
    return config


@app.command()
def collect_cmd(
    config_path: str = typer.Option(DEFAULT_CONFIG_PATH, "--config", "-c", help="Path to config file"),
    dry_run: bool = typer.Option(DEFAULT_DRY_RUN, "--dry-run", help="Dry run mode"),
    verbose: bool = typer.Option(DEFAULT_VERBOSE, "--verbose", "-v", help="Verbose output"),
):
    """
    Collect syndication links from RSS feeds.

    Esegue il raccoglimento dei link di sindacazione dai feed RSS configurati.
    Legge i feed definiti nel file di configurazione e estrae i post che
    contengono link al blog.
    """
    config = get_config(config_path, dry_run, verbose)
    collect(config)


@app.command()
def add_cmd(
    config_path: str = typer.Option(DEFAULT_CONFIG_PATH, "--config", "-c", help="Path to config file"),
    dry_run: bool = typer.Option(DEFAULT_DRY_RUN, "--dry-run", help="Dry run mode"),
    verbose: bool = typer.Option(DEFAULT_VERBOSE, "--verbose", "-v", help="Verbose output"),
):
    """
    Add syndication links to blog posts.

    Aggiunge i link di sindacazione ai post del blog confrontando i feed RSS
    raccolti con i post esistenti nel blog e aggiornando i metadati con i
    riferimenti alle fonti originali.
    """
    config = get_config(config_path, dry_run, verbose)
    add(config)


@app.command()
def correct_cmd(
    config_path: str = typer.Option(DEFAULT_CONFIG_PATH, "--config", "-c", help="Path to config file"),
    dry_run: bool = typer.Option(DEFAULT_DRY_RUN, "--dry-run", help="Dry run mode"),
    verbose: bool = typer.Option(DEFAULT_VERBOSE, "--verbose", "-v", help="Verbose output"),
):
    """
    Correct missing source links in JSON files using Mastodon API.

    Correggie i link sorgente mancanti nei file JSON dei post utilizzando
    l'API di Mastodon per recuperare i post originali e ricostruire i
    riferimenti mancanti.
    """
    config = get_config(config_path, dry_run, verbose)
    correct(config)


@app.command()
def all_cmd(
    config_path: str = typer.Option(DEFAULT_CONFIG_PATH, "--config", "-c", help="Path to config file"),
    dry_run: bool = typer.Option(DEFAULT_DRY_RUN, "--dry-run", help="Dry run mode"),
    verbose: bool = typer.Option(DEFAULT_VERBOSE, "--verbose", "-v", help="Verbose output"),
):
    """
    Run collect, add, correct, and replay commands in sequence.

    Esegue in sequenza tutti i comandi del workflow di sindacazione:
    1. collect - raccoglie i link dai feed RSS
    2. add - aggiunge i link ai post del blog
    3. correct - corregge i link mancanti via API
    4. replay - genera le anteprime dei reply
    """
    config = get_config(config_path, dry_run, verbose)

    typer.echo("Running collect...")
    collect(config)

    typer.echo("Running add...")
    add(config)

    typer.echo("Running correct...")
    correct(config)

    typer.echo("Running replay...")
    replay(config)

    typer.secho("All commands completed!", fg=typer.colors.GREEN)


@app.command()
def replay_cmd(
    config_path: str = typer.Option(DEFAULT_CONFIG_PATH, "--config", "-c", help="Path to config file"),
    dry_run: bool = typer.Option(DEFAULT_DRY_RUN, "--dry-run", help="Dry run mode"),
    verbose: bool = typer.Option(DEFAULT_VERBOSE, "--verbose", "-v", help="Verbose output"),
):
    """
    Process reply links in posts and generate previews.

    Elabora i link dei reply nei post e genera le anteprime dei contenuti
    provenienti dai social media, creando una visualizzazione integrata
    dei post originali e delle relative risposte.
    """
    config = get_config(config_path, dry_run, verbose)
    replay(config)


@app.command()
def tag_cmd(
    filepath: str = typer.Argument(None, help="Specific file to process (optional)"),
    config_path: str = typer.Option(DEFAULT_CONFIG_PATH, "--config", "-c", help="Path to config file"),
    dry_run: bool = typer.Option(DEFAULT_DRY_RUN, "--dry-run", help="Dry run mode"),
    verbose: bool = typer.Option(DEFAULT_VERBOSE, "--verbose", "-v", help="Verbose output"),
    force: bool = typer.Option(False, "--force", "-f", help="Process all files even if they already have keywords"),
):
    """
    Generate SEO keywords for posts using AI and add them to frontmatter.

    Genera parole chiave SEO per i post utilizzando un modello AI (llama3)
    e le aggiunge al frontmatter Hugo nella sezione keywords.
    """
    config = get_config(config_path, dry_run, verbose)
    tagger(config, filepath, config.options.dry_run, force)


if __name__ == "__main__":
    app()
