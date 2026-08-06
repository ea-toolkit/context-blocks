import { useActiveBlock } from '../../lib/active-block';
import BlockOntology from '../studio/BlockOntology';
import OntologySchema, { type OntologySchemaProps } from './OntologySchema';

/** The Ontology view: baked build-time schema by default, or the active block's
 * ontology LIVE from the Studio API when `?block=<name>` is set. */
export default function OntologyView(baked: OntologySchemaProps) {
  const block = useActiveBlock();
  if (block) return <BlockOntology block={block} />;
  return <OntologySchema {...baked} />;
}
